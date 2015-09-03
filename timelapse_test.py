total_runtime = '00:01:00'
hours, minutes, seconds = total_runtime.split(':')
hours, minutes, seconds = int(hours), int(minutes), int(seconds)
seconds += (hours * 3600) + (minutes * 60)
print('Time until dusk: {}'.format(seconds))
