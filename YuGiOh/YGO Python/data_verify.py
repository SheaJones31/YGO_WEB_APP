def dict_key_print(card_dict):
    for set_data, set_value in card_dict.items():
        print(f"{set_data}: {set_value}")


def data_print(data):
    for card in data['data']:
        for attr, values in card.items():
            if attr == "card_sets":
                print(attr, values)
                for value in values:
                    dict_key_print(value)
                pass

            elif attr == "card_images":
                print(attr, values)
                for value in values:
                    dict_key_print(value)
                pass

            elif attr == "card_prices":
                print(attr, values)
                for value in values:
                    dict_key_print(value)
                pass

            else:
                print(f"{attr}: {card[attr]}")
                pass
