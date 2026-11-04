"""Approved 12 native customers, Endesga 64. Standard library, independent of proposals."""
from pathlib import Path
import json
SOURCE=Path(__file__).with_name('customers-native.json')
def load_cast():
    data=json.loads(SOURCE.read_text(encoding='utf-8'))
    assert data['size']==[96,120] and len(data['customers'])==12
    assert len({p['id'] for p in data['customers']})==12
    for i,p in enumerate(data['customers']):
        allowed=set(p['colors'])|{'.'}
        assert len(p['pixels'])==120
        assert all(len(row)==96 and set(row)<=allowed for row in p['pixels'])
        assert p['facing']==('left' if i%2 else 'right')
    return data
