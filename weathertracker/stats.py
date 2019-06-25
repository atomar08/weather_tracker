from werkzeug.exceptions import abort
from weathertracker.measurement_store import query_measurements

def get_stats(stats, metrics, from_datetime, to_datetime):
   stats_lis = []
   # stats_lis = {}

   if from_datetime >= to_datetime:
      return stats_lis

   selected_measurement_lis = query_measurements(from_datetime, to_datetime)

   for metric in metrics:
      print("for metric {}".format(metric))
      # initialize
      response_stats_dic = {}
      measurement = selected_measurement_lis[0]
      all_values_for_avg = []
      if metric in measurement.metrics:
         initial_value = measurement.get_metric(metric)
         all_values_for_avg.append(initial_value)
      else:
         initial_value = 0

      # initialize metric_stats_dic with very first measurement
      print("initializing stats for {}".format(metric))
      for stat in stats:
         print("setting stat {}".format(stat))
         response_stats_dic[stat] = initial_value

      index = 1
      while index < len(selected_measurement_lis):
         print("now finding stats using all {}".format(index))
         measurement = selected_measurement_lis[index]

         if metric in measurement.metrics:
            value = measurement.get_metric(metric)
            print("metric next value {}".format(value))
         else:
            value = 0

         # Assuming that if metric value is zero, skip metric value for min, max, average calculation
         if value == 0:
            print("skipping, value is 0")
            index += 1
            continue

         if 'min' in response_stats_dic and response_stats_dic['min'] > value:
            response_stats_dic['min'] = value

         if 'max' in response_stats_dic and response_stats_dic['max'] < value:
            response_stats_dic['max'] = value

         if 'average' in response_stats_dic:
            print("adding in average {}".format(value))
            all_values_for_avg.append(value)
         index += 1

      if 'average' in response_stats_dic:
         print("total sum {} and count {}".format(sum(all_values_for_avg), len(all_values_for_avg)))
         response_stats_dic['average'] = round((sum(all_values_for_avg) / len(all_values_for_avg)), 1)

      # response format:
      stats_lis.append({metric: response_stats_dic})  # declare stats_lis = [] at top
      # stats_lis[metric] = response_stats_dic  # declare stats_lis = {}  at top

   print("Stats list {}".format(stats_lis))
   return stats_lis
