from collections import defaultdict
from pydantic import BaseModel


class DataSet(BaseModel):
    label: str
    c_type: str
    data: list
    fill: bool
    backgroundColor: str
    borderColor: str


class TimeSeries(BaseModel):
    labels: list
    datasets: list
    options: dict


class ProposalAnalytics:
    @staticmethod
    def index_votes_by_date(votes):
        groups = defaultdict(list)
        for obj in votes:
            groups[str(obj["timestamp"])] += [obj]
        return groups

    @staticmethod
    def daily_power_distribution(bat):
        dist = dict(
            for_sum_pwr=0,
            ast_sum_pwr=0,
            for_sum_cnt=0,
            ast_sum_cnt=0
        )
        for item in bat:
            if item["support"]:
                dist["for_sum_pwr"] += int(item["votingPower"])
                dist["for_sum_cnt"] += 1
            else:
                dist["ast_sum_pwr"] += int(item["votingPower"])
                dist["ast_sum_cnt"] += 1
        return dist

    @staticmethod
    def get_daily_distributions(data):
        daily_power_dist = defaultdict(dict)
        for timestamp, batch in data.items():
            daily_power_dist[timestamp] = \
                ProposalAnalytics.daily_power_distribution(batch)
        return daily_power_dist

    @staticmethod
    def cumulative_sum(dists):
        total_v_supply = 16000000000000000000000000
        precision = 10000
        for_pwr_counter = 0
        ast_pwr_counter = 0
        f_votes_ct = 0
        a_votes_ct = 0
        cumulative_data = defaultdict(dict)
        for timestamp, dist in dists.items():
            for_pwr_counter += ((dist["for_sum_pwr"] / total_v_supply) * precision)
            ast_pwr_counter += ((dist["ast_sum_pwr"] / total_v_supply) * precision)
            f_votes_ct += dist["for_sum_cnt"]
            a_votes_ct += dist["ast_sum_cnt"]
            cumulative_data[timestamp] = dict(
                for_cummulative=for_pwr_counter,
                for_count=f_votes_ct,
                against_cummulative=ast_pwr_counter,
                against_count=a_votes_ct,
            )
        return cumulative_data

    @staticmethod
    def create_datasets(data):
        datasets = []
        for val in list(data.values()):
            params = dict()
            params["data_index"] = []
            for key, inner_val in list(val.items()):
                params['label'] = str(key)
                params['data_index'] += [inner_val]
                if 'count' in key:
                    params["c_type"] = 'bar'
                    if 'for' in key:
                        params['backgroundColor'] = 'rgb(54, 162, 235)'
                        params['borderColor'] = 'white'
                    elif 'against' in key:
                        params['backgroundColor'] = 'rgb(255, 99, 132)'
                    else:
                        params['backgroundColor'] = 'black'
                else:
                    params["c_type"] = 'line'
                    params["borderWidth"] = 2
                    if 'for' in key:
                        params['borderColor'] = 'rgba(54, 162, 235, 0.2)'
                        params['fill'] = True
                    elif 'against' in key:
                        params['borderColor'] = 'rgba(255, 99, 132, 0.2)'
                        params['fill'] = True
                    else:
                        params['borderColor'] = 'black'
                        params['fill'] = False
                d_set = DataSet.construct(**params).dict()
                datasets.append(d_set)
        return datasets

    @staticmethod
    def create_snapshot_series(votes):
        self = ProposalAnalytics
        indexed = self.index_votes_by_date(votes)
        print("indexed", dict(indexed))
        daily = self.get_daily_distributions(indexed)
        print("daily", dict(indexed))
        data = self.cumulative_sum(daily)
        print("cumulative", data)
        datasets = self.create_datasets(data)
        labels = list(data.keys())
        options = dict(
            scales=dict(
                yAxes=[
                    dict(
                        ticks=dict(
                            beginAtZero=True,
                        )
                    )
                ]
            )
        )
        time_series = TimeSeries(
            labels=labels,
            datasets=datasets,
            options=options
        )
        return time_series.dict()

