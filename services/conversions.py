from models.transaction import TransactionsModel


def add_transaction(db, transaction_registry: dict):
    """
    Add a new transaction to the database.

    Parameters:
        - db (object): the db session
        - transaction_registry (dict): the transaction information
    """
    aux = transaction_registry.get("metadata", None)
    transaction_registry.pop("metadata", None)

    transaction_registry["time_of_conversion"] = aux["time_of_conversion"]
    transaction_registry["from_currency"] = aux["from_currency"]
    transaction_registry["to_currency"] = aux["to_currency"]

    new_transaction = TransactionsModel(**transaction_registry)
    db.add(new_transaction)
    db.commit()


def get_transactions(db):
    """
    Get all the transactions from the database

    Parameters:
        - db (object): the db session
    Returns:
        - r (list): the list of transactions
    """
    r = db.query(TransactionsModel).all()
    return r
