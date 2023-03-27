from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
 

class Trader:
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        This method takes a TradingState object as input and outputs a dictionary of
        lists of Order objects that represent the trader's desired trades.

        :param state: a TradingState object containing all market data
        :return: a dictionary of lists of Order objects representing the desired trades
        """
        result = {}

        for product in state.order_depths.keys():
            if product == 'PEARLS':
                order_depth: OrderDepth = state.order_depths[product]
                orders: List[Order] = []
                fair_price = self.calculate_fair_price(product, order_depth)
                if fair_price is None:
                    continue

                # Check for any buy orders that are willing to pay more than the fair price
                for price, volume in order_depth.buy_orders.items():
                    if price >= fair_price:
                        break
                    orders.append(Order(product, price, -volume))

                # Check for any sell orders that are willing to sell for less than the fair price
                for price, volume in order_depth.sell_orders.items():
                    if price <= fair_price:
                        break
                    orders.append(Order(product, price, volume))

                result[product] = orders

        return result

    def calculate_fair_price(self, product: str, order_depth: OrderDepth) -> float:
        """
        This method calculates the fair price for a given product and OrderDepth.

        :param product: the name of the product
        :param order_depth: an OrderDepth object containing the current buy and sell orders for the product
        :return: a float representing the fair price, or None if it cannot be calculated
        """
        if len(order_depth.buy_orders) == 0 or len(order_depth.sell_orders) == 0:
            return None

        # Calculate the average of the highest bid and lowest ask prices
        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        fair_price = (best_bid + best_ask) / 2
        return fair_price
