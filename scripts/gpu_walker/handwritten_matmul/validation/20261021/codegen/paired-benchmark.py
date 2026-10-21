#!/usr/bin/env python3
"""Replay real Jac packed graphs and compare fresh handwritten dense CUDA kernels.

Requires only NumPy, nvcc, and the CUDA driver. Jac inputs/outputs are checked
against saved hashes and an independent dense oracle. No Jac compiler import is
needed to replay. Every arm computes every output of the selected case.
"""
import argparse, ctypes as c, hashlib, json, random, statistics, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
class Driver:
 def __init__(self,device=0):
  self.lib=c.CDLL('libcuda.so.1');self.allocs=[];self.modules=[];self.graphs=[]
  signatures={
   'cuInit':[c.c_uint],'cuDeviceGet':[c.POINTER(c.c_int),c.c_int],
   'cuDevicePrimaryCtxRetain':[c.POINTER(c.c_void_p),c.c_int], 'cuCtxSetCurrent':[c.c_void_p],
   'cuDevicePrimaryCtxRelease_v2':[c.c_int], 'cuDeviceGetName':[c.c_char_p,c.c_int,c.c_int],
   'cuMemGetInfo_v2':[c.POINTER(c.c_size_t),c.POINTER(c.c_size_t)],
   'cuMemAlloc_v2':[c.POINTER(c.c_uint64),c.c_size_t], 'cuMemFree_v2':[c.c_uint64],
   'cuMemcpyHtoD_v2':[c.c_uint64,c.c_void_p,c.c_size_t], 'cuMemcpyDtoH_v2':[c.c_void_p,c.c_uint64,c.c_size_t],
   'cuModuleLoad':[c.POINTER(c.c_void_p),c.c_char_p], 'cuModuleUnload':[c.c_void_p],
   'cuModuleGetFunction':[c.POINTER(c.c_void_p),c.c_void_p,c.c_char_p],
   'cuStreamCreate':[c.POINTER(c.c_void_p),c.c_uint],'cuStreamDestroy_v2':[c.c_void_p],
   'cuStreamSynchronize':[c.c_void_p],'cuStreamBeginCapture':[c.c_void_p,c.c_int],
   'cuStreamEndCapture':[c.c_void_p,c.POINTER(c.c_void_p)],
   'cuGraphInstantiateWithFlags':[c.POINTER(c.c_void_p),c.c_void_p,c.c_uint64],
   'cuGraphLaunch':[c.c_void_p,c.c_void_p], 'cuGraphExecDestroy':[c.c_void_p], 'cuGraphDestroy':[c.c_void_p],
   'cuEventCreate':[c.POINTER(c.c_void_p),c.c_uint],'cuEventRecord':[c.c_void_p,c.c_void_p],
   'cuEventSynchronize':[c.c_void_p],'cuEventElapsedTime':[c.POINTER(c.c_float),c.c_void_p,c.c_void_p],
   'cuEventDestroy_v2':[c.c_void_p],
   'cuLaunchKernel':[c.c_void_p,*([c.c_uint]*7),c.c_void_p,c.POINTER(c.c_void_p),c.c_void_p]}
  for n,t in signatures.items():getattr(self.lib,n).argtypes=t;getattr(self.lib,n).restype=c.c_int
  self.call('cuInit',0);self.device=c.c_int();self.call('cuDeviceGet',c.byref(self.device),device)
  self.ctx=c.c_void_p();self.call('cuDevicePrimaryCtxRetain',c.byref(self.ctx),self.device)
  self.call('cuCtxSetCurrent',self.ctx)
  self.stream=c.c_void_p();self.call('cuStreamCreate',c.byref(self.stream),1)
  self.events=[]
  for _ in range(2):
   e=c.c_void_p();self.call('cuEventCreate',c.byref(e),0);self.events.append(e)
  name=c.create_string_buffer(256);self.call('cuDeviceGetName',name,256,self.device);self.name=name.value.decode()
 def call(self,n,*a):
  result=getattr(self.lib,n)(*a)
  if result:raise RuntimeError(f'{n}: CUDA driver error {result}')
 def memory(self):
  free,total=c.c_size_t(),c.c_size_t();self.call('cuMemGetInfo_v2',c.byref(free),c.byref(total));return {'free':free.value,'total':total.value}
 def upload(self,a):
  a=np.ascontiguousarray(a);p=c.c_uint64();self.call('cuMemAlloc_v2',c.byref(p),max(a.nbytes,8));self.allocs.append(p.value)
  if a.nbytes:self.call('cuMemcpyHtoD_v2',p,a.ctypes.data,a.nbytes)
  return p.value
 def download(self,p,shape,dtype):
  a=np.empty(shape,dtype=dtype);self.call('cuMemcpyDtoH_v2',a.ctypes.data,p,a.nbytes);return a
 def kernel(self,path,name):
  mod=c.c_void_p();self.call('cuModuleLoad',c.byref(mod),str(path).encode());self.modules.append(mod)
  fn=c.c_void_p();self.call('cuModuleGetFunction',c.byref(fn),mod,name.encode());return fn
 def capture(self,fn,grid,block,holders,inner):
  params=(c.c_void_p*len(holders))(*(c.addressof(v) for v in holders))
  def launch():self.call('cuLaunchKernel',fn,*grid,*block,0,self.stream,params,None)
  # Prime module/JIT before capture and timing.
  launch();self.call('cuStreamSynchronize',self.stream)
  self.call('cuStreamBeginCapture',self.stream,0)
  for _ in range(inner):launch()
  graph=c.c_void_p();self.call('cuStreamEndCapture',self.stream,c.byref(graph))
  exe=c.c_void_p();self.call('cuGraphInstantiateWithFlags',c.byref(exe),graph,0);self.graphs.append((graph,exe))
  return exe
 def measure(self,exe,inner):
  self.call('cuEventRecord',self.events[0],self.stream);self.call('cuGraphLaunch',exe,self.stream)
  self.call('cuEventRecord',self.events[1],self.stream);self.call('cuEventSynchronize',self.events[1])
  ms=c.c_float();self.call('cuEventElapsedTime',c.byref(ms),*self.events);return ms.value*1000/inner
 def clear_case(self):
  for graph,exe in self.graphs:self.call('cuGraphExecDestroy',exe);self.call('cuGraphDestroy',graph)
  self.graphs=[]
  for p in reversed(self.allocs):self.call('cuMemFree_v2',p)
  self.allocs=[]
 def close(self):
  self.clear_case()
  for mod in reversed(self.modules):self.call('cuModuleUnload',mod)
  for e in self.events:self.call('cuEventDestroy_v2',e)
  self.call('cuStreamDestroy_v2',self.stream);self.call('cuDevicePrimaryCtxRelease_v2',self.device)

def artifact_path(text,base):
 p=Path(text)
 if p.is_file():return p
 # Existing manifests predate the move into ~/jaseci/jac-on-gpu.
 for marker in ['dist/','scripts/']:
  if marker in text:
   q=ROOT/text[text.index(marker):]
   if q.is_file():return q
 q=base/p.name
 if q.is_file():return q
 raise FileNotFoundError(text)
def load(info,base):
 p=artifact_path(info['path'],base)
 if sha(p)!=info['sha256']:raise ValueError(f'Hash mismatch: {p}')
 typ={'q':'<i8','I':'<u4','Q':'<u8','d':'<f8'}[info['type']]
 a=np.fromfile(p,dtype=typ)
 if len(a)!=info['count']:raise ValueError(f'Count mismatch: {p}')
 return a

def prepare_arm(d,fn,arrays,args,grid,block,inner):
 ptrs=[d.upload(a) for a in arrays];holders=[c.c_uint64(v) for v in ptrs]+args
 return d.capture(fn,grid,block,holders,inner),ptrs

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--inputs',type=Path,default=ROOT/'dist/gpu-cursor-concat-20261007/benchmark/inputs.json')
 p.add_argument('--ptx',type=Path);p.add_argument('--output',type=Path,required=True)
 p.add_argument('--jac-variant',action='append',default=[],metavar='NAME=PTX',help='Additional Jac PTX arm, interleaved with the baseline in each round')
 p.add_argument('--warmup',type=int,default=5);p.add_argument('--repeats',type=int,default=25);p.add_argument('--inner',type=int,default=16)
 p.add_argument('--seed',type=int,default=928);p.add_argument('--nvcc',default='/usr/local/cuda-12.9/bin/nvcc')
 p.add_argument('--dense-shapes',nargs='*',default=[])
 a=p.parse_args()
 if a.warmup<0 or min(a.repeats,a.inner)<1:p.error('Invalid repetition counts')
 a.output.mkdir(parents=True,exist_ok=True)
 nvcc_cmd=[a.nvcc,'-ptx','-O3','-arch=compute_86','-std=c++17',str(HERE/'matmul.cu'),'-o',str(a.output/'matmul.ptx')]
 subprocess.run(nvcc_cmd,check=True)
 source=json.loads(a.inputs.read_text());cases=[r for r in source['cases'] if r['kind']=='matmul']
 ptx=a.ptx or a.inputs.parent/'Dot.ptx'
 variants={'':ptx}
 for variant in a.jac_variant:
  label,path=variant.split('=',1)
  if not label or label in variants:p.error('Jac variant names must be nonempty and unique')
  variants[label]=Path(path)
 result={'runner_sha256':sha(Path(__file__)),'timestamp_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'nvcc_version':subprocess.check_output([a.nvcc,'--version'],text=True),'dtype':'int64','measurement':'CUDA-event graph replay time / inner; includes GPU graph scheduling gaps','warmup':a.warmup,'repeats':a.repeats,'inner':a.inner,'seed':a.seed,'input_manifest':str(a.inputs.resolve()),'input_sha256':sha(a.inputs),'jac_ptx':str(ptx),'jac_ptx_sha256':sha(ptx),'jac_variants':{label:{'path':str(path.resolve()),'sha256':sha(path)} for label,path in variants.items()},'cuda_source_sha256':sha(HERE/'matmul.cu'),'nvcc_command':nvcc_cmd,'cases':[],'records':[]}
 try:result['gpu_before']=subprocess.check_output(['nvidia-smi'],text=True)
 except subprocess.CalledProcessError:result['gpu_before']='nvidia-smi failed'
 d=Driver();result['gpu_name']=d.name;result['memory_before']=d.memory()
 try:
  jac_functions={label:d.kernel(path,'jac_Dot_cursors_batch') for label,path in variants.items()}
  functions={n:d.kernel(a.output/'matmul.ptx','matmul_'+n+'_i64') for n in ['naive','tiled']}
  for text in a.dense_shapes:
   shape=[int(v) for v in text.split('x')]
   if len(shape)!=3 or min(shape)<1:raise ValueError(text)
   cases.append({'id':'dense-only-'+text,'shape':shape,'dense_only':True})
  for case in cases:
   m,k,n=case['shape'];lanes=m*n
   A=np.fromfunction(lambda i,q:(i+q)%7-3,(m,k),dtype=np.int64).astype(np.int64)
   B=np.fromfunction(lambda q,j:(q*3+j)%11-5,(k,n),dtype=np.int64).astype(np.int64)
   # Magnitudes <=3 and <=5: all multiply/accumulate intermediates <=15*K.
   if 15*k>np.iinfo(np.int64).max:raise OverflowError('Input bound exceeds int64')
   expected=A@B;meta={'id':case['id'],'shape':[m,k,n],'outputs':lanes,'MACs':m*k*n,'dense_only':case.get('dense_only',False),'A_sha256':hashlib.sha256(A.tobytes()).hexdigest(),'B_sha256':hashlib.sha256(B.tobytes()).hexdigest(),'expected_sha256':hashlib.sha256(expected.tobytes()).hexdigest(),'arms':{}}
   if not meta['dense_only']:
    saved=load(case['expected'],a.inputs.parent/case['id']).reshape(m,n)
    np.testing.assert_array_equal(saved,expected)
   arms={};outputs={};statuses={}
   for label,fn in functions.items():
    exe,ptrs=prepare_arm(d,fn,[A,B,np.full((m,n),-999,dtype=np.int64)],[c.c_int(m),c.c_int(k),c.c_int(n)],((n+15)//16,(m+15)//16,1),(16,16,1),a.inner)
    arms['CUDA '+label]=exe;outputs['CUDA '+label]=ptrs[-1]
   if not meta['dense_only']:
    for layout in case['layouts']:
     arr=[load(f,a.inputs.parent/case['id']) for f in layout['files']]
     # Verify dense inputs by following EACH saved cursor chain, not the filename.
     values,tags,offsets,targets,heads,counts=arr[:6];nodes=len(tags)
     if not np.all(counts==1) or not np.all(arr[6]==0):raise ValueError('Only zero-initialized, single-seed Dot fixtures supported')
     ai=heads[:lanes].copy();bi=heads[lanes:].copy()
     for q in range(k):
      if np.any(ai<0) or np.any(bi<0):raise ValueError('Short input chain')
      np.testing.assert_array_equal(values[ai],np.repeat(A[:,q],n))
      np.testing.assert_array_equal(values[bi],np.tile(B[q,:],m))
      for cur,channel in [(ai,0),(bi,1)]:
       rows=channel*(nodes+1)+cur;begin=offsets[rows];end=offsets[rows+1]
       if not np.all(end-begin==(1 if q<k-1 else 0)):raise ValueError('Unexpected chain degree')
       cur[:]=targets[begin] if q<k-1 else -1
     arr[7]=np.full(lanes,-999,dtype=np.int64);arr[8]=np.full(lanes,0xffffffff,dtype=np.uint32)
     args=[c.c_uint64(v) for v in [nodes,len(targets),lanes,layout['queue_capacity'],layout['max_visits']]]
     for variant,jac_fn in jac_functions.items():
      label='Jac '+(variant+' ' if variant else '')+layout['label']
      exe,ptrs=prepare_arm(d,jac_fn,arr,args,((lanes+127)//128,1,1),(128,1,1),a.inner)
      arms[label]=exe;outputs[label]=ptrs[7];statuses[label]=ptrs[8]
   poison=np.ascontiguousarray(np.bitwise_not(expected))
   bad_status=np.full(lanes,0xffffffff,dtype=np.uint32)
   for phase,rounds in [('warmup',a.warmup),('measured',a.repeats)]:
    for pair in range(rounds):
     order=list(arms);random.Random(a.seed+pair+(10000 if phase=='measured' else 0)).shuffle(order)
     for label in order:
      # Poison outside the event interval to detect a replay that fails to write.
      d.call('cuMemcpyHtoD_v2',outputs[label],poison.ctypes.data,poison.nbytes)
      if label in statuses:d.call('cuMemcpyHtoD_v2',statuses[label],bad_status.ctypes.data,bad_status.nbytes)
      us=d.measure(arms[label],a.inner)
      actual=d.download(outputs[label],(m,n),np.int64);np.testing.assert_array_equal(actual,expected)
      if label in statuses:np.testing.assert_array_equal(d.download(statuses[label],lanes,np.uint32),np.zeros(lanes,dtype=np.uint32))
      result['records'].append({'case':case['id'],'arm':label,'phase':phase,'pair':pair,'event_us_per_launch':us,'outputs_checked':lanes})
   for label in arms:
    vals=[r['event_us_per_launch'] for r in result['records'] if r['case']==case['id'] and r['arm']==label and r['phase']=='measured']
    meta['arms'][label]={'median_us':statistics.median(vals),'min_us':min(vals),'max_us':max(vals),'sample_n':len(vals)}
   meta['all_outputs_and_statuses_verified']=True;result['cases'].append(meta);d.clear_case()
   write(a.output/'results.json',result);print(json.dumps(meta),flush=True)
  result['memory_after']=d.memory();result['complete']=True
 finally:
  d.close();write(a.output/'results.json',result)
 try:result['gpu_after']=subprocess.check_output(['nvidia-smi'],text=True)
 except subprocess.CalledProcessError:result['gpu_after']='nvidia-smi failed'
 write(a.output/'results.json',result)
if __name__=='__main__':main()
