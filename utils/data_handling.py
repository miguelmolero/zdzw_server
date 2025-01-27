from models.statistics_data import StatisticsData
from models.filter_payload import OrderFilters, OrderDirection, OrderType
from typing import List

def order_data(data: StatisticsData, order_filters: OrderFilters) -> StatisticsData:
    reverse = order_filters.order_direction == OrderDirection.ORDER_DIRECTION_DESCENDING
    
    sort_by = ""
    match order_filters.order_type:
        case OrderType.ORDER_TYPE_PASS:
            sort_by = "pass_count"
        case OrderType.ORDER_TYPE_FAIL:
            sort_by = "fail_count"
        case OrderType.ORDER_TYPE_INVALID:
            sort_by = "invalid_count"
        case _:
            return data 

    for factory_stats in data.factory_stats:
        factory_stats.device_stats.sort(
            key=lambda device: getattr(device, sort_by), reverse=reverse
        )

    data.factory_stats.sort(
        key=lambda factory: getattr(factory.factory_data, sort_by), reverse=reverse
    )

    return data
