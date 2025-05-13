
def build_filter(params : dict) -> str :
    filters = []
    
    def parse_in_clause(key):
        if(params.get(key)):
            values = [f"'{val.strip()}'" for val in params[key].split(',')]
            filters.append(f"{key.capitalize()} IN ({', '.join(values)})")
            
    for attr in ['shape','color','purity','cut','polish','symm','fls','culet','country']:
        parse_in_clause(attr)
        
    if(params['cts']):
        cts_filters = []
        
        for r in params['cts'].split(','):
            try:                
                if '-' in r:
                    from_val, to_val = map(float, r.split('-'))
                    if from_val is not None and to_val is not None:
                        cts_filters.append(f"Cts BETWEEN toDecimal32({from_val},2) AND toDecimal32({to_val},2)")
                else:
                    from_val = float(r)
                    cts_filters.append(f"Cts >= toDecimal32({from_val},2)")
            except ValueError:
                    continue
        
        if cts_filters:
                filters.append(f"({' OR '.join(cts_filters)})")
                
    def range_clause(range,col):
        try:
            from_val, to_val = map(float,range.strip().split("-"))
            db_col = col
            if(col == 'depth_per'):
                db_col = 'Depth_'
            elif(col == 'table_per'):
                db_col = 'Table_'
            else:
                db_col = col.capitalize()

            if from_val is not None and to_val is not None:
                filters.append(f"{db_col} BETWEEN toDecimal32({from_val},2) AND toDecimal32({to_val},2)")
            elif from_val is not None:
                filters.append(f"{db_col} >= {from_val}")
            elif to_val is not None:
                filters.append(f"{db_col} <= {to_val}")
        except Exception as e:
            print({"error" : str(e)})
            
    for attr in ['length','width','depth','depth_per','table_per']:
        if(params[attr]):
            range_clause(params[attr],attr)
            
    return " AND ".join(filters) if filters else "1"
    
    
            
    