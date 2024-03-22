

def sku_generator(self, prefix):
    sku_parts = [prefix]

    # Adding product Brand to SKU
    sku_parts.append(self.prod_brand.sku_part)
    
    # Adding category to SKU
    sku_parts.append(self.prod_category.sku_part)

    # Adding variant to SKU if available, otherwise use "NA"
    if self.prod_variant:
        sku_parts.append(self.prod_variant.sku_part)
    else:
        sku_parts.append("NA")

    # Adding unit size to SKU if available, otherwise use "NA"
    if self.prod_unit_size:
        sku_parts.append(self.prod_unit_size.sku_part)
    else:
        sku_parts.append("NA")

    # Adding product ID to SKU
    sku_parts.append(str(self.prod_id))

    # Combining the SKU parts into the final SKU code
    sku_code = '-'.join(sku_parts)

    return sku_code