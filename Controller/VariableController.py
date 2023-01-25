
class VariableController:
    def return_lowest_value_in_dict(self, dict):
        target = float('inf')
        for key in dict:
            if dict[key] < target:
                target = dict[key]
        return target

    def return_all_keys_of_value(self, dict, value):
        keys = []
        for sub_key in dict:
            if dict[sub_key] == value:
                keys.append(sub_key)
        return keys