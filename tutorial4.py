from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order


class Trader:
    PEARLS_LIMIT = 20
    BANANAS_LIMIT = 20

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}

        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():

            # Check if the current product is either PEARLS or BANANAS, only then run the order logic
            if product in ['PEARLS', 'BANANAS']:

                # Retrieve the Order Depth containing all the market BUY and SELL orders for the product
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # Define a fair value for the product.
                # If the product is PEARLS, the value is 1
                # If the product is BANANAS, the value is the average of the last 5 prices
                if product == 'PEARLS':
                    acceptable_price = 1
                else:
                    acceptable_price = (max(order_depth.buy_orders.keys()) + min(order_depth.sell_orders.keys())) / 2

                # Retrieve the current position for the product
                current_position = state.positions[product]

                # Calculate the maximum position allowed for the product
                max_position = self.PEARLS_LIMIT if product == 'PEARLS' else self.BANANAS_LIMIT

                # If we have reached our position limit, we should not trade anymore
                if abs(current_position) == max_position:
                    continue

                # If statement checks if there are any SELL orders in the market
                if len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    # Check if the lowest ask (sell order) is lower than the above defined fair value
                    if best_ask < acceptable_price:

                        # Calculate the maximum quantity that we can buy or sell
                        max_quantity = max_position - abs(current_position)

                        # Determine the quantity to trade
                        trade_quantity = min(best_ask_volume, max_quantity)

                        # In case the lowest ask is lower than our fair value,
                        # This presents an opportunity for us to buy cheaply
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with the same quantity
                        # We expect this order to trade with the sell order
                        print("BUY", str(-trade_quantity) + "x", best_ask)
                        orders.append(Order(product, best_ask, -trade_quantity))

                # The below code block is similar to the one above,
                # the difference is that it finds the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > acceptable_price:
                    # Calculate the maximum quantity that we can buy or sell
                        max_quantity = max_position - abs(current_position)

                # Determine the quantity to trade
                        trade_quantity = min(best_bid_volume, max_quantity)

                # Send a SELL order at the price level of the bid,
                # with the same quantity
                # We expect this order to trade with the buy order
                        print("SELL", str(trade_quantity) + "x", best_bid)
                        orders.append(Order(product, best_bid, trade_quantity))

            # Add the orders for the current product to the output dictionary
                result[product] = orders
                
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
    # Return the output dictionary
        return result


                       
