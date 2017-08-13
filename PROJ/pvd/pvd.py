from __future__ import absolute_import
import math
from utils import get_range_tuple

class PixelValueDifferencing:

    @classmethod
    def apply_method(cls, px, py, data_value):
        """
        Applies pixel value differencing method and returns modified pixel values
        """
        difference = math.fabs(px-py)
        lower, upper, width, t = get_range_tuple(difference)

        if len("{0:b}".format(data_value))>t:
            raise ValueError("{value} should not take more that {t} bits.".format(value=data_value, t=t))

        t_dash = data_value
        d_dash = t_dash + lower

        p_dash_x, p_dash_y = cls._substitution(px, py, difference, d_dash)
        return cls._adjust_boundary(p_dash_x, p_dash_y)

    @classmethod    
    def _substitution(cls, px, py, d, d_dash):
        """
        Adjust difference between two pixels to embed data acoording to pixel value differencing method
        """
        m = math.fabs(d - d_dash)
        m_ceil = math.ceil(m/2.0)
        m_floor = math.floor(m/2.0) 
        
        if d < d_dash:
            # Increase distance between px and py - i.e - (subtract from smaller pixel value), + (add to larger pixel value)
            if px < py:
                return (px - m_floor), (py + m_ceil)
            else:
                return (px + m_ceil), (py - m_floor)
        else:
            # Decrease distance between px and py
            if px < py:
                return (px + m_ceil), (py - m_floor) 
            else:
                return (px - m_ceil), (py + m_floor)

    @classmethod
    def _adjust_boundary(cls, p_dash_x, p_dash_y):
        """
        Handle boundary value condition
        """
        if p_dash_x>255:
            val = p_dash_x - 255
            return 255, p_dash_y-val
        elif p_dash_y>255:
            val = p_dash_y - 255
            return p_dash_x-val, 255
        elif p_dash_x<0:
            val = math.fabs(p_dash_x)
            return 0, p_dash_y + val
        elif p_dash_y<0:
            val = math.fabs(p_dash_y)
            return p_dash_x+val, 0
        
        return p_dash_x, p_dash_y


    @classmethod
    def retrieve_data(cls, px, py, binary_flag=False):
        """
        Retrieves and returns embeded data in two consecutive pixels
        """
        difference = math.fabs(px-py)
        lower, upper, width, t = get_range_tuple(difference)
        data_value = difference - lower
        return "{0:b}".format(data_value) if binary_flag else data_value