from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

def filtering_smartphones_by_price(all_smartphones_in_once, maximumPrice, filteredSmartphones) :
    for smartphone in all_smartphones_in_once:
        reformattedPrice = smartphone['productPrice'].replace(',', '')
        smartphonePrice = float(reformattedPrice.split()[0])
        if smartphonePrice <= maximumPrice:
            filteredSmartphones.append(smartphone)

def filtering_smartphones_by_selected_brands(all_smartphones_in_once, filteredSmartphonesBySelectedBrand, selected_brands) :
    for smartphone in all_smartphones_in_once :
        if smartphone['productBrand'] in selected_brands:
            filteredSmartphonesBySelectedBrand.append(smartphone)


def filtering_smartphones_by_brands_and_price(
                    all_smartphones_in_once,
                    filteredSmartphonesByBrandsMaximumPrice,
                    selected_brands,
                    maximumPrice
                ) :
    for smartphone in all_smartphones_in_once:
        # The presence of a ',' in the smartphone price poses a problems when converting the
        # string price to a float value for good comparison.
        reformattedPrice = smartphone['productPrice'].replace(',', '')

        # Convertinng The price after changing the ',' with nothing
        smartphonePrice = float(reformattedPrice.split()[0])

        if smartphone['productBrand'] in selected_brands and smartphonePrice <= maximumPrice:
            filteredSmartphonesByBrandsMaximumPrice.append(smartphone)

def index(request, page = None):
    smartphones_brands_file = open('scrapping/smartphones_&_brands.json', 'r', 1, 'utf8')

    # The Data Coming From My JSON File Is Of Type String
    smartphones_brands_string = smartphones_brands_file.readlines()

    # With eval() Method Ican Change The Type Of My Data Inside The Variable {smartphones_brands_string} To A py Dict
    smartphones_brands_dict = eval(smartphones_brands_string[0])

    # Getting All The Products All In One Time
    all_smartphones_in_once = []
    for i in range(1, 15) :
        for product in smartphones_brands_dict[f"page_{i}"]:
            all_smartphones_in_once.append(product)


    # Getting The Products Page By Page Depends On What The User choose
    smartphones = []
    if page is not None :
        for product in smartphones_brands_dict[f"page_{page}"]:
            smartphones.append(product)
    else :
        page = 1
        for product in smartphones_brands_dict[f"page_{page}"]:
            smartphones.append(product)

    brands = smartphones_brands_dict['brands']

    smartphones_brands_file.close();

    if request.POST :
        if request.POST.get('brands') is None and request.POST.get('maximumPrice') == '' :
            return render(request, 'smartphones/index.html', {
                        'smartphones': smartphones,
                        'brands': brands,
                        'results': smartphones_brands_dict['productsCounter'],
                        'selectedBrands': [],
                        'pages': range(1, 15),
                        'page': page,
                        'priceValue': ''
                    })
        else :
            if request.POST.get('brands') is None and request.POST.get('maximumPrice') != '':
                maximumPrice = float(request.POST.get('maximumPrice'))
                filteredSmartphonesByMaxPrice = []
                filtering_smartphones_by_price(all_smartphones_in_once, maximumPrice, filteredSmartphonesByMaxPrice)
                return render(request, 'smartphones/index.html', {
                    'smartphones': filteredSmartphonesByMaxPrice,
                    'brands': brands,
                    'results': len(filteredSmartphonesByMaxPrice),
                    'selectedBrands': [],
                    'pages': range(1, 15),
                    'page': page,
                    'priceValue': maximumPrice
                })

            if request.POST.get('brands') is not None and request.POST.get('maximumPrice') == '':
                selected_brands = request.POST.getlist('brands')
                filteredSmartphonesBySelectedBrand = []
                filtering_smartphones_by_selected_brands(all_smartphones_in_once, filteredSmartphonesBySelectedBrand, selected_brands)
                return render(request, 'smartphones/index.html', {
                    'smartphones': filteredSmartphonesBySelectedBrand,
                    'brands': brands,
                    'results': len(filteredSmartphonesBySelectedBrand),
                    'selectedBrands': selected_brands,
                    'pages': range(1, 15),
                    'page': page,
                    'priceValue': ''
                })

            if request.POST.get('brands') is not None and request.POST.get('maximumPrice') != '':
                selected_brands = request.POST.getlist('brands')
                maximumPrice = float(request.POST.get('maximumPrice'))
                filteredSmartphonesByBrandsMaximumPrice = []

                filtering_smartphones_by_brands_and_price(
                    all_smartphones_in_once,
                    filteredSmartphonesByBrandsMaximumPrice,
                    selected_brands,
                    maximumPrice
                )

                return render(request, 'smartphones/index.html', {
                    'smartphones': filteredSmartphonesByBrandsMaximumPrice,
                    'brands': brands,
                    'results': len(filteredSmartphonesByBrandsMaximumPrice),
                    'selectedBrands': selected_brands,
                    'pages': range(1, 15),
                    'page': page,
                    'priceValue': maximumPrice
                })

    else :
        return render(request, 'smartphones/index.html', {
            'smartphones': smartphones,
            'brands': brands,
            'results': smartphones_brands_dict['productsCounter'],
            'selectedBrands': [],
            'pages': range(1, 15),
            'page': page,
            'priceValue': ''
        })