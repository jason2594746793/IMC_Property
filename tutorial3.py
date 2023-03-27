from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order


class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}

        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():

            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product in ['PEARLS', 'BANANAS']:

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # Define a fair value for the PEARLS.
                # In this case, let's use the mid-price between the best bid and best ask
                if len(order_depth.buy_orders) > 0 and len(order_depth.sell_orders) > 0:
                    fair_value = (max(order_depth.buy_orders.keys()) + min(order_depth.sell_orders.keys())) / 2
                else:
                    # If there are no buy or sell orders, set the fair value to 0
                    fair_value = 0

                # If statement checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    # Check if the lowest ask (sell order) is lower than the fair value
                    if best_ask < fair_value:

                        # In case the lowest ask is lower than our fair value,
                        # This presents an opportunity for us to buy cheaply
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with the same quantity
                        # We expect this order to trade with the sell order
                        print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_volume))

                # The below code block is similar to the one above,
                # the difference is that it finds the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if len(order_depth.buy_orders) > 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > fair_value:

                        # If there are already buy orders present at the fair value,
                        # add to the volume of the highest buy order
                        if fair_value in order_depth.buy_orders:
                            print("ADD", str(best_bid_volume) + "x", fair_value)
                            orders.append(Order(product, fair_value, best_bid_volume))
                        else:
                            # Otherwise, send a new buy order at the fair value
                            print("BUY", str(best_bid_volume) + "x", fair_value)
                            orders.append(Order(product, fair_value, best_bid_volume))

                # Add all the above orders to the result dict
                result[product] = orders
        return result