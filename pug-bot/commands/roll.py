from .checks import *

from ..config import *
from random import randint

@check(invalid_range, have_no_pug)
async def roll(message, pugs, user_input, client):
    roll_range = user_input["arguments"].split()    
    await message.channel.send(f"randint(roll_range[0], roll_range[1])")