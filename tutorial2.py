from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order


class Trader:

    def __init__(self):
        self.fair_values = {}  # Dictionary to store fair values for each product
        self.last_prices = {}  # Dictionary to store last traded prices for each product

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}

        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():

            # Retrieve the Order Depth containing all the market BUY and SELL orders for the current product
            order_depth: OrderDepth = state.order_depths[product]

            # Initialize the list of Orders to be sent as an empty list
            orders: list[Order] = []

            # Update the last traded price for the product
            self.last_prices[product] = state.last_prices[product]

            # Compute a new fair value for the product
            self.fair_values[product] = self.compute_fair_value(product, order_depth)

            # Only trade the current product if the fair value is known
            if self.fair_values[product] is not None:

                # If there are any SELL orders in the market
                if len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price, and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    # Check if the lowest ask (sell order) is lower than the fair value
                    if best_ask < self.fair_values[product]:

                        # In case the lowest ask is lower than our fair value,
                        # This presents an opportunity for us to buy cheaply
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with the same quantity
                        # We expect this order to trade with the sell order
                        print(f"BUY {product} {str(-best_ask_volume)}x {best_ask}")
                        orders.append(Order(product, best_ask, -best_ask_volume))

                # If there are any BUY orders in the market
                if len(order_depth.buy_orders) > 0:

                    # Sort all the available buy orders by their price, and select only the buy order with the highest price
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]

                    # Check if the highest bid (buy order) is higher than the fair value
                    if best_bid > self.fair_values[product]:

                        # In case the highest bid is higher than our fair value,
                        # This presents an opportunity for us to sell at a premium
                        # The code below therefore sends a SELL order at the price level of the bid,
                        # with the same quantity
                        # We expect this order to trade with the buy order
                        print(f"SELL {product} {str(best_bid_volume)}x {best_bid}")
                        orders.append(Order(product, best_bid, -best_bid_volume))

                # Add all the above orders to the result dict
                result[product] = orders

        # Return the dict
        return result