from dataclasses import dataclass,asdict
@dataclass(frozen=True)
class Finding:
 path:str; breaking:bool; reason:str
 def as_dict(self):return asdict(self)
def compare(old,new,path=''):
 out=[]; ot=old.get('type'); nt=new.get('type')
 if ot!=nt: out.append(Finding(path or '/',True,f'type changed {ot!r} -> {nt!r}')); return out
 if 'enum' in old or 'enum' in new:
  a=set(old.get('enum',[])); b=set(new.get('enum',[])); removed=a-b; added=b-a
  if removed: out.append(Finding(path or '/',True,'enum values removed: '+','.join(map(str,sorted(removed,key=str)))))
  if added: out.append(Finding(path or '/',False,'enum values added: '+','.join(map(str,sorted(added,key=str)))))
 if ot=='object':
  op=old.get('properties',{}); np=new.get('properties',{}); orq=set(old.get('required',[])); nrq=set(new.get('required',[]))
  for k in sorted(orq-nrq): out.append(Finding(f'{path}/{k}',False,'field no longer required'))
  for k in sorted(nrq-orq): out.append(Finding(f'{path}/{k}',True,'field became required'))
  for k in sorted(op.keys()-np.keys()): out.append(Finding(f'{path}/{k}',True,'property removed'))
  for k in sorted(np.keys()-op.keys()): out.append(Finding(f'{path}/{k}',False,'optional property added' if k not in nrq else 'required property added'))
  for k in sorted(op.keys()&np.keys()): out.extend(compare(op[k],np[k],f'{path}/{k}'))
 for key,strict in [('minimum','higher'),('maximum','lower')]:
  if key in old and key in new:
   br=(new[key]>old[key]) if key=='minimum' else (new[key]<old[key]); ch=new[key]!=old[key]
   if ch: out.append(Finding(path or '/',br,f'{key} changed {old[key]} -> {new[key]}'))
 return out
