# -*- coding: utf-8 -*-

###
# Copyright (c) 2013, Aaron Toponce
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

from supybot.commands import *
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

import thefuckingweather

class FWeather(callbacks.Plugin):
    """
    This plugin has one command to return the weather from
    http://thefuckingweather.com.
    """
    def fw(self, irc, msg, args, text):
        """<text>

        INVALID FUCKING INPUT. PLEASE ENTER A FUCKING ZIP CODE, OR A FUCKING
        CITY-STATE PAIR.
        """
        if text:
            try:
                w = thefuckingweather.get_weather(text)
                location = w['location']
                f_temp = w['current']['temperature']
                c_temp = round((5.0/9.0)*(f_temp-32), 1)
                weather = w['current']['weather'][0]
                remark = w['current']['remark']
                comment = "{0}: {1}°F, {2}°C?! {3}! ({4})".format(location, f_temp, c_temp, weather, remark)
            except thefuckingweather.LocationError:
                comment = "I CAN'T FIND THAT SHIT!"
            except thefuckingweather.ParseError:
                comment = "I CAN'T PARSE THE FUCKING WEATHER!"

        irc.reply(comment)

    fw = wrap(fw, ['text'])

Class = FWeather

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
