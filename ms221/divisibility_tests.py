# -*- coding: utf-8 -*-

# .        :       ...    :::::::-.   ...    ::: :::    .,::::::    :::::::-.
# ;;,.    ;;;   .;;;;;;;.  ;;,   `';, ;;     ;;; ;;;    ;;;;''''     ;;,   `';,
# [[[[, ,[[[[, ,[[     \[[,`[[     [[[['     [[[ [[[     [[cccc      `[[     [[
# $$$$$$$$"$$$ $$$,     $$$ $$,    $$$$      $$$ $$'     $$""""       $$,    $$
# 888 Y88" 888o"888,_ _,88P 888_,o8P'88    .d888o88oo,.__888oo,__     888_,o8P'
# MMM  M'  "MMM  "YMMMMMP"  MMMMP"`   "YmmMMMM""""""YUMMM""""YUMMM    MMMMP"`


class DivisibilityTests(object):
    """
        Module D2, Page 15 - 18

        Tests for dividing by a particular number up to 14. Now obviously
        just calling mod on x with m would do the same job but these spell
        out the steps explicitly as expected in the exam.
    """

    def __init__(self):
        pass

    def digits(self, number, reverse=True):
        """
            Returns the digits of number in order as a list. Many of the tests
            involve manipulating the supplied number in such a way
        """
        num_str = str(number)
        if reverse:
            num_str = reversed(num_str)

        return [int(x, 10) for x in num_str]

    def digit_sum(self, x, modulus):
        """
            Returns the sum of digits successivly until the sum is under
            9 - used for testing by 3, 9
        """

        _sum = sum(self.digits(x, reverse=False))
        print "\tDigit sum: %d" % _sum

        if _sum > 9:
            return self.digit_sum(_sum, modulus)
        else:
            r = _sum % modulus
            print "Finished, remainder: %d\n" % r
            return r

    def inflate_digits(self, x):
        """
            Takes a list of digits and returns the number they represent
            if in order of powers of 10, so [1, 2] becomes 21.
        """
        return sum([d * 10**i for i, d in enumerate(x)])

    def alternating_sum(self, digits, offset=0):
        """
            Returns the sum of the digits but alternated in sign. Setting
            offset to 1 will result in the _first_ term being negated.
        """
        return sum([(-1) ** (i + offset) * d for i, d in enumerate(digits)])

    def grouped_by_sums(self, x, modulus, n=3):
        """
            Essentially the algorithim for divisibility by 7 and 13
        """
        digits = str(x)[::-1]  # Reverse the string form of x
        # Create groupings of 3 of each number. We use the reversed digit string
        # so that the range works nicely going up rather than backwards even
        # when the length isn't divisible by 3. This also means we need to
        # reverse again the resultant groups of digits
        groups = [digits[i:i + n][::-1] for i in range(0, len(digits), n)]
        # Now we can get the modulus of these after casting to int
        group_modN = [int(x, 10) % modulus for x in groups]
        print "Grouped digits %r mod %d: %r" % (groups, modulus, group_modN)
        alternating_sum = self.alternating_sum(group_modN)
        r = alternating_sum % modulus
        print "Alternating sum: %d, remainder: %d" % (alternating_sum, r)
        return r

    def by_2(self, x):
        """
            A number is divisible by 2 if the _last_ digit is
            divisible by 2
        """
        return self.digits(x)[0] % 2

    def by_3(self, x):
        """
            Module D2, Page 15

            A simple test for divisibility by 3 involves forming the sum of
            the digits of the given number. If the resulting digit sum has
            more than one digit, then the process is repeated until a single
            digit remains. The original number is divisible by 3 if and only
            if this single digit is divisible by 3.
        """

        print "Dividing %d by 3" % x
        return self.digit_sum(x, 3)

    def by_4(self, x):
        """
            This just needs to check the last _two_ digits (as opposed to one
            in the case of by_2)
        """
        # Remember, the returned digits are reversed so we need the first two
        # (they're in order of size, 10**0, 10**1, 10**2, etc)
        first_two_digits = self.inflate_digits(self.digits(x)[:2])
        r = (first_two_digits)  % 4
        print "Dividing %d by 4 - checking %d: %d" % (x, first_two_digits, r)
        return r

    def by_5(self, x):
        first_digit = self.digits(x)[0]
        r = (first_digit)  % 5
        print "Dividing %d by 5 - checking %d: %d" % (x, first_digit, r)
        return r

    def by_6(self, x):
        """
            Module D2, Page 18

            This involves testing the remainder by 2 and 3 and then using that
            info to get the remainder mod 6. The module text suggests using
            the following congreuence:

                r6 ≡ 3r2 − 2r3 (mod 6).
        """
        r2, r3 = self.by_2(x), self.by_3(x)
        val = (3 * r2 - 2 * r3)
        r6 = val % 6
        print "Dividing %d by 6, congruence relation: %d gives %d" % (x, val, r6)
        return r6

    def by_7(self, x):
        """
            Module D2, Page 19

            These ones involve the alternating digit sum mod 13 of groups of
            3. This is based on the following factorization of 1001:

                1001 = 7 × 11 × 13

            Which implies that 1000 ≡ −1 (mod 7 and 13). A similar argument
            to that of the by_11 case then applies.
        """
        return self.grouped_by_sums(x, 7)

    def by_8(self, x):
        """
            This just needs to check the last _three_ digits - like by_4, by_2
        """
        last_three_digits = self.inflate_digits(self.digits(x)[:3])
        r = (last_three_digits)  % 8
        print "Dividing %d by 8 - check %d: %d" % (x, last_three_digits, r)
        return r

    def by_9(self, x):
        """
            Module D2, Page 16, Activity 2.2

            The digit sum method depends on congruences (2.1) and these
            congruences also hold modulo 9, because 10 ≡ 1 (mod 9). Therefore
            the digit sum method works for division by 9.
        """
        print "Dividing %d by 9" % x
        return self.digit_sum(x, 9)

    def by_11(self, x):
        """
            Module D2, Page 16

            This uses the fact that 10 ≡ −1 (mod 11), from which we deduce
            that 10k ≡ (−1)k (mod 11), for k = 1, 2, . . . .

            Therefore, if a = a0 + a1 × 10 + a2 × 102 + · · · + am × 10m ,
            then a ≡ a0 − a1 + a2 − · · · + (−1)m am (mod 11).

            a has the same remainder on division by 11 as the alternating digit
            sum, which starts with the _units_ digit.

            This *could* be really big and be repeatedly applied again and again
            much like the by_3, by_9 examples but we'll forget about that for
            the purposes of this!
        """

        print "Dividing %d by 11" % x

        # We start by getting the digits in the order of least signifigant first
        digits = self.digits(x, reverse=True)
        alternating_sum = self.alternating_sum(digits)
        r = alternating_sum % 11

        print "Alternating sum: %d gives %d" % (alternating_sum, r)
        return r

    def by_12(self, x):
        """
            Module D2, Page 18

            This uses a similar technique to that of by_6 only using the
            tests for 3 and 4. This time we use the following relation:

                r12 ≡ 4r3 − 3r4 (mod 12)
        """

    def by_13(self, x):
        return self.grouped_by_sums(x, 13)
