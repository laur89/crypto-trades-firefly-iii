import src.exchanges.impls as impls
from src.exchanges.exchange_interface import CryptoExchangeInterface


def get_available_exchanges():
    # get all classes from impls module and check for sub-classes of CryptoExchangeModuleMetaClass
    pass


def get_specific_exchange_interface(trading_platform: str) -> CryptoExchangeInterface:
    for instance in impls.list_of_impl_meta_class_instances:
        if trading_platform == instance.get_exchange_name():
            return instance.get_exchange_client()

    raise Exception("The exchange \"" + trading_platform + "\" is not supported by now!")
