import os
class Simpledb:
    def __init__(self, datafile):
        self.datafile=datafile
        f=open(datafile, 'a')
        f.close()
        
    def __repr__(self):
        return ('<'+'Simpledb'+' file=\''+self.datafile+'\'>')

    def insert(self, key, value):
        f=open(self.datafile, 'a')
        f.write(key + '\t' + value + '\n')
        f.close()

    def select_one(self,key):
        f=open(self.datafile, 'r')
        for row in f:
            (k,v)=row.split('\t',1)
            if k == key:
                return v[:-1]
        f.close()

    def delete(self, key):
        f=open(self.datafile, 'r')
        result = open('result.txt', 'w')
        for (row) in f:
            (k, v) = row.split('\t', 1)
            if k != key:
                result.write(row)
            else:
                found=True
        f.close()
        result.close()
        import os
        os.replace('result.txt', self.datafile)

    def update(self, key, value):
        f=open(self.datafile, 'r')
        result = open('result.txt', 'w')
        for (row) in f:
            (k, v) = row.split('\t', 1)
            if k == key:
                result.write(key+'\t'+value+'\n')
            else:
                result.write(row)
        f.close()
        result.close()
        import os
        os.replace('result.txt', self.datafile)
