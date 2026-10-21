#!/usr/bin/env python3
"""Build real shared Jac graphs with the existing packer for the CUDA comparison."""
import argparse, hashlib, json, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE.parent))
from compare_named_layouts import prepare_case, schemas_and_modules
from compare_layouts import memory_context

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
 p.add_argument('--shapes',nargs='+',default=['3x5x2','17x31x19','64x128x64','128x128x128','256x256x256'])
 a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 schemas,modules=schemas_and_modules({'Dot'});schema=schemas['Dot']
 (a.output/'Dot.ptx').write_text(schema.ptx)
 cases=[]
 with memory_context():
  for text in a.shapes:
   shape=tuple(int(v) for v in text.split('x'))
   if len(shape)!=3 or min(shape)<1:raise ValueError(text)
   case,_=prepare_case('matmul',shape,schemas,modules,[928],a.output,1)
   cases.append(case);print(case['id'],case['nodes'],flush=True)
 manifest={'cases':cases,'origin':'Real Jac Scalar/RowNext/ColumnNext objects and existing production pack_cursors','node_unit':'one int64 value','ptx_sha256':hashlib.sha256(schema.ptx.encode()).hexdigest(),'source_sha256':hashlib.sha256((ROOT/'jac/examples/gpu/named_cursors.jac').read_bytes()).hexdigest()}
 (a.output/'inputs.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
