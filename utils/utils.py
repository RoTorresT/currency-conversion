def rebuild_metadata(data: dict):
    """
    This function takes in a dictionary of a conversion registry and
    modifies it to include a new key 'metadata' that contains
    the time of conversion, from currency, and to currency.
    It also removes the original keys for time_of_conversion,
    from_currency and to_currency

    Args:
        - data (dict): dict from the conversion database table

    Returns:
        - data (dict): same data but with the new metadata key
            containing the time of conversion, from currency, and to currency
    """

    data.pop("id", None)
    data["metadata"] = {
        "time_of_conversion": data["time_of_conversion"],
        "from_currency": data["from_currency"],
        "to_currency": data["to_currency"],
    }
    data.pop("time_of_conversion", None)
    data.pop("from_currency", None)
    data.pop("to_currency", None)
    return data
