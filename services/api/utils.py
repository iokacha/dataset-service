import pandas as pd
import datetime


TYPES_VALIDATOR = {
    "int"       : lambda i: int(i),
    "string"    : lambda i: str(i),
    "date"      : lambda d: datetime.datetime.strptime(d, '%Y-%m-%d')
}



def validator(record, schema):
    for col,value in record.items():
        try : 
            column_type = schema[col] 
            TYPES_VALIDATOR[column_type](value)
        except Exception as e:
            return False
    return True


def upload_dataset(filepath, schema, separator):
    raw_data = pd.read_csv(filepath, sep=separator)
    raw_data["__is_valid"] = raw_data.apply(lambda record: validator(dict(record), schema), axis=1)
    raw_data["__created_at"] = datetime.datetime.now()

    return list(raw_data.T.to_dict().values())


def csvify(content_list, separator='|') :
    df = pd.DataFrame(content_list)
    rdf = df[df['__is_valid'] == True]
    printable_cols = [c for c in rdf.columns if not c.startswith('__')]
    return rdf[printable_cols].to_csv(sep=separator, index = False)