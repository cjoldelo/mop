from django.core.management.base import BaseCommand
from tom_dataproducts.models import ReducedDatum
from tom_targets.models import Target
from astropy.time import Time
from mop.toolbox import fittools
from mop.brokers import gaia as gaia_mop


import json
import numpy as np
import datetime
import os

class Command(BaseCommand):

    help = 'Fit an event with PSPL and parallax, then ingest fit parameters in the db'
    
    def add_arguments(self, parser):
        parser.add_argument('target_name', help='name of the event to fit')
        parser.add_argument('--cores', help='Number of workers to use', default=os.cpu_count(), type=int)

    
    def handle(self, *args, **options):

       target, created = Target.objects.get_or_create(name= options['target_name'])
       try:	
          
           if 'Gaia' in target.name:

               gaia_mop.update_gaia_errors(target)

           datasets = ReducedDatum.objects.filter(target=target)

           time = [Time(i.timestamp).jd for i in datasets if i.data_type == 'photometry']
           phot = []
           for data in datasets:
               if data.data_type == 'photometry':
                    try:
                         phot.append([data.value['magnitude'],data.value['error'],data.value['filter']])
               
                    except:
                         # Weights == 1
                         phot.append([data.value['magnitude'],1,data.value['filter']])
                   
                  

           photometry = np.c_[time,phot]


        

           t0_fit,u0_fit,tE_fit,piEN_fit,piEE_fit,mag_source_fit,mag_blend_fit,mag_baseline_fit,cov,model = fittools.fit_PSPL_parallax(target.ra, target.dec, photometry, cores = options['cores'])

           #Add photometry model
           
           model_time = datetime.datetime.strptime('2018-06-29 08:15:27.243860', '%Y-%m-%d %H:%M:%S.%f')
           data = {'lc_model_time': model.lightcurve_magnitude[:,0].tolist(),
           'lc_model_magnitude': model.lightcurve_magnitude[:,1].tolist()
                    }
           existing_model =   ReducedDatum.objects.filter(source_name='MOP',data_type='lc_model',
                                                          timestamp=model_time,source_location=target.name)

                                                            
           if existing_model.count() == 0:     
                rd, created = ReducedDatum.objects.get_or_create(
                                                                    timestamp=model_time,
                                                                    value=data,
                                                                    source_name='MOP',
                                                                    source_location=target.name,
                                                                    data_type='lc_model',
                                                                    target=target)                  

                rd.save()

           else:
                rd, created = ReducedDatum.objects.update_or_create(
                                                                    timestamp=existing_model[0].timestamp,
                                                                    value=existing_model[0].value,
                                                                    source_name='MOP',
                                                                    source_location=target.name,
                                                                    data_type='lc_model',
                                                                    target=target,
                                                                    defaults={'value':data})                  

                rd.save()
                  

           time_now = Time(datetime.datetime.now()).jd
           how_many_tE = (time_now-t0_fit)/tE_fit
          

           if how_many_tE>2:

              alive = False

           else:
     
              alive = True
           
           last_fit = Time(datetime.datetime.utcnow()).jd
           extras = {'Alive':alive, 't0':t0_fit,'u0':u0_fit,'tE':tE_fit,
                         'piEN':piEN_fit,'piEE':piEE_fit,
                         'Source_magnitude':mag_source_fit,
                         'Blend_magnitude':mag_blend_fit,
                         'Baseline_magnitude':mag_baseline_fit,
                         'Fit_covariance':json.dumps(cov.tolist()),
                         'Last_Fit':last_fit}
           target.save(extras = extras)
       except:
           pass

       

