#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
from telethon.extensions import markdown

from .. import loader, utils

from requests import get


def register(cb):
    cb(CurrencyRateMod())


class CurrencyRateMod(loader.Module):
    """Converts currency rate"""

    def __init__(self):
        self.commands = {"cr": self.crcmd}
        self.config = loader.ModuleConfig("DEFAULT_CURRENCY", "USD", "Currency to convert to by default",
                                          "API_KEY", "", "API key from https://free.currencyconverterapi.com")
        self.name = _("Currency")

    async def crcmd(self, message):
        """
        Usage: .cr amount from to
        Example: .cr 1 USD EGP  
        """
        if self.config["API_KEY"] is None:
            await message.edit(_("<code>Please provide an API key via the configuration mode.</code>"))
            return
        args = utils.get_args(message)
        if len(args) == 3:
            amount = args[0]
            currency_from = args[1].upper()
            currency_to = args[2].upper()
        elif len(args) == 2:
            amount = args[0]
            currency_from = args[1].upper()
            currency_to = self.config['DEFAULT_CURRENCY']
        else:
            await message.edit(_("Usage: .cr amount from to"))
            return
        value = get(
            f"https://free.currconv.com/api/v7/convert?apiKey={self.config['API_KEY']}&q="
            f"{currency_from}_{currency_to}&compact=ultra").json()[f'{currency_from}_{currency_to}']
        result = round(float(amount) * value, 5)
        await message.edit((
            f"**{amount} {currency_from}** is: **{result} {currency_to}**"), parse_mode=markdown)
