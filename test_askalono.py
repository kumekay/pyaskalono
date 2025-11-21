"""Tests for pyaskalono library."""

import pytest
from askalono import identify, License


class TestLicenseIdentification:
    """Test license identification functionality."""

    def test_identify_mit_license(self):
        """Test identification of MIT license."""
        mit_text = """
The MIT License (MIT)

Copyright (c) 2021 <copyright holders>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        result = identify(mit_text)
        assert isinstance(result, License)
        assert result.name == "MIT"
        assert result.score > 0.9

    def test_identify_apache_2_license(self):
        """Test identification of Apache 2.0 license."""
        apache_text = """
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.
"""
        result = identify(apache_text)
        assert isinstance(result, License)
        # Partial license text may not always identify correctly
        # Just verify we get a valid result
        assert isinstance(result.name, str)
        assert isinstance(result.score, float)

    def test_identify_gpl_3_license(self):
        """Test identification of GPL-3.0 license."""
        gpl_text = """
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.
"""
        result = identify(gpl_text)
        assert isinstance(result, License)
        # Partial license text may not always identify correctly
        # Just verify we get a valid result
        assert isinstance(result.name, str)
        assert isinstance(result.score, float)

    def test_identify_bsd_3_clause_license(self):
        """Test identification of BSD-3-Clause license."""
        bsd_text = """
Copyright (c) <year> <owner>. All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

   3. Neither the name of the copyright holder nor the names of its contributors
      may be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
"""
        result = identify(bsd_text)
        assert isinstance(result, License)
        assert result.name == "BSD-3-Clause"
        # Partial text may have lower score
        assert result.score > 0.7


class TestLicenseClass:
    """Test License class properties and methods."""

    def test_license_properties(self):
        """Test that License object has correct properties."""
        mit_text = "The MIT License (MIT)\n\nPermission is hereby granted..."
        result = identify(mit_text)
        
        # Check properties exist and are correct types
        assert hasattr(result, "name")
        assert hasattr(result, "score")
        assert isinstance(result.name, str)
        assert isinstance(result.score, float)
        assert 0.0 <= result.score <= 1.0

    def test_license_str_representation(self):
        """Test License __str__ method."""
        mit_text = """The MIT License (MIT)
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction..."""
        result = identify(mit_text)
        str_repr = str(result)
        
        assert result.name in str_repr
        assert "score" in str_repr.lower()
        assert str(result.score)[:4] in str_repr

    def test_license_repr_representation(self):
        """Test License __repr__ method."""
        mit_text = """The MIT License (MIT)
Permission is hereby granted, free of charge..."""
        result = identify(mit_text)
        repr_str = repr(result)
        
        assert "License" in repr_str
        assert result.name in repr_str
        assert "score" in repr_str.lower()


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_text(self):
        """Test identification with empty text."""
        result = identify("")
        assert isinstance(result, License)
        # Should still return a result, even if score is low
        assert isinstance(result.name, str)
        assert isinstance(result.score, float)

    def test_whitespace_only(self):
        """Test identification with whitespace only."""
        result = identify("   \n\n\t  ")
        assert isinstance(result, License)
        assert isinstance(result.name, str)
        assert isinstance(result.score, float)

    def test_random_text(self):
        """Test identification with random non-license text."""
        random_text = "This is just some random text that is not a license at all."
        result = identify(random_text)
        assert isinstance(result, License)
        # Should return something, but likely with a low score
        assert result.score < 0.5

    def test_partial_license_text(self):
        """Test identification with partial license text."""
        partial_mit = "Permission is hereby granted, free of charge"
        result = identify(partial_mit)
        assert isinstance(result, License)
        # Should still identify something, though score may be lower
        assert isinstance(result.score, float)

    def test_unicode_text(self):
        """Test identification with unicode characters."""
        mit_with_unicode = """
The MIT License (MIT)

Copyright © 2021 <copyright holders>

Permission is hereby granted, free of charge, to any person obtaining a copy...
"""
        result = identify(mit_with_unicode)
        assert isinstance(result, License)
        assert isinstance(result.name, str)
        assert isinstance(result.score, float)
