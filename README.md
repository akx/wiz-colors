# wiz-colors

Named colors from the [WiZ Connected](https://www.wizconnected.com/en-MY/consumer/app/) Android app.

## usage

You can find pre-extracted data in the repository.

* colors.tsv: name, hex color as TSV
* colors.json: name to hex color map
* colors.html: a visual guide to colors

### advanced

If you want to extract the data yourself, you'll need to put `values.xml`, `strings.xml` and `NamedColorHelper.smali` (found by applying baksmali to the `classes2.dex` file in the APK) in the `input/` directory, then run `extract_colors.py` with Python 3.8 +.

## license

The color data could be intellectual property of Signify Holding, the parent company of WiZ. Use at your own discretion.

The extraction code is licensed under the MIT license.

> Copyright 2021 Aarni Koskela
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
