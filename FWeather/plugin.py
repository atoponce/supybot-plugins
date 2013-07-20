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
    
    def _color(self, deg, u):
        """Colorize the temperature. Use the same scale as
        https://github.com/reticulatingspline/Supybot-Weather to match that
        plugin, in case it is also loaded. Code copyright spline, with my
        modifications."""

        # first, convert into F so we only have one table.
        if u == 'c':   # celcius, convert to farenheit, make float
            deg = deg * 9.0/5.0 + 32

        # determine color
        if deg < 10.0:
            color = 'light blue'
        elif 10.0 <= deg <= 32.0:
            color = 'teal'
        elif 32.1 <= deg <= 50.0:
            color = 'blue'
        elif 50.1 <= deg <= 60.0:
            color = 'light green'
        elif 60.1 <= deg <= 70.0:
            color = 'green'
        elif 70.1 <= deg <= 80.0:
            color = 'yellow'
        elif 80.1 <= deg <= 90.0:
            color = 'orange'
        else:
            color = 'red'

        # return
        if u == 'f':    # no need to convert back
            return ircutils.mircColor("{0}°F".format(deg), color)
        elif u == 'c':    # convert back
            return ircutils.mircColor("{0}°C".format((deg - 32) * 5/9), color)

    ### FIXME
    #def fw(self, irc, msg, args, opts, text):
    def fw(self, irc, msg, args, text):
        """<text>

        INVALID FUCKING INPUT. PLEASE ENTER A FUCKING ZIP CODE, OR A FUCKING
        CITY-STATE PAIR.
        """
        if text:
            try:
                w = thefuckingweather.get_weather(text)
                ### FIXME
                #if opts:
                #    for (key, val) in opts:
                #        if key == 'metric':
                #            unit = 'c'
                #        else:
                #            unit = 'f'
                #        if key == 'forecast':
                #            forecast = {}
                #            f = w['forecast']
                #            for k,v in forecast:
                #                if k == 'high' or k == 'low':
                #                    forecast[k] = self._color(v,unit)
                #                else:
                #                    forecast[k] = v
                location = ircutils.mircColor(w['location'], 'white')
                f_temp = self._color(w['current']['temperature'], 'f')
                c_temp = self._color(round((5.0/9.0)*(w['current']['temperature']-32), 1), 'c')
                weather = w['current']['weather'][0]
                remark = w['current']['remark']
                comment = "{0}: {1}, {2}?! {3}! ({4})".format(location, f_temp, c_temp, weather, remark)
            except thefuckingweather.LocationError:
                comment = "I CAN'T FIND THAT SHIT!"
            except thefuckingweather.ParseError:
                comment = "I CAN'T PARSE THE FUCKING WEATHER!"

        irc.reply(comment)
        ### FIXME
        #if forecast:
        #    irc.reply("{0}/{1}".format())

    ### FIXME
    #fw = wrap(fw, [getopts({'forecast':'','metric':''}), ['text'])
    fw = wrap(fw, ['text'])

Class = FWeather

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
