from rest_framework_csv.renderers import CSVRenderer


class ControlCSVRenderer(CSVRenderer):
    header = ['name', 'type', 'maximum_rabi_rate', 'polar_angle']
