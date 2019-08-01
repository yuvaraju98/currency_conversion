

from jchart import Chart

class LineChart(Chart):
    chart_type = 'line'

    def __init__(self, values):
        super(LineChart, self).__init__()
        self.value_array=values

    def get_datasets(self, **kwargs):
        # print("aaaa",self.value_array)

        return [{
            'label': "My Dataset",
            'data': self.value_array
        }
        ]
