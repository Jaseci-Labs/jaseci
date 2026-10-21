; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-p6:32:32-i64:64-i128:128-i256:256-v16:16-v32:32-n16:32:64"
target triple = "nvptx64-nvidia-cuda"

define ptx_kernel void @jac_Dot_cursors_batch(ptr addrspace(1) %values, ptr addrspace(1) %type_tags, ptr addrspace(1) %offsets, ptr addrspace(1) %targets, ptr addrspace(1) %heads, ptr addrspace(1) %seed_counts, ptr addrspace(1) %initial_total, ptr addrspace(1) %results, ptr addrspace(1) %status, ptr addrspace(1) %queue, i64 %node_count, i64 %edge_count, i64 %walker_count, i64 %queue_capacity, i64 %max_visits) {
entry:
  %.17 = call i32 @llvm.nvvm.read.ptx.sreg.ctaid.x()
  %.18 = zext i32 %.17 to i64
  %.19 = call i32 @llvm.nvvm.read.ptx.sreg.ntid.x()
  %.20 = zext i32 %.19 to i64
  %.21 = call i32 @llvm.nvvm.read.ptx.sreg.tid.x()
  %.22 = zext i32 %.21 to i64
  %.23 = mul i64 %.18, %.20
  %index = add i64 %.23, %.22
  %.24 = icmp ult i64 %index, %walker_count
  br i1 %.24, label %start, label %done

start:                                            ; preds = %entry
  %.27 = getelementptr i64, ptr addrspace(1) %initial_total, i64 %index
  %.28 = load i64, ptr addrspace(1) %.27, align 8
  %.40 = mul i64 0, %walker_count
  %.41 = add i64 %.40, %index
  %.42 = getelementptr i64, ptr addrspace(1) %seed_counts, i64 %.41
  %.43 = load i64, ptr addrspace(1) %.42, align 8
  %.44 = icmp ugt i64 %queue_capacity, 0
  %.45 = icmp ule i64 %.43, %queue_capacity
  %.46 = and i1 %.44, %.45
  br i1 %.46, label %seed.valid, label %error.6

round.check:                                      ; preds = %seed.valid.1, %advance
  %.31.0 = phi i64 [ 0, %seed.valid.1 ], [ %.121, %advance ]
  %.32.0 = phi i64 [ %.51, %seed.valid.1 ], [ %.32.1, %advance ]
  %.33.0 = phi i64 [ %.71, %seed.valid.1 ], [ %.33.1, %advance ]
  %.34.0 = phi i64 [ %.43, %seed.valid.1 ], [ %.34.1, %advance ]
  %.35.0 = phi i64 [ %.63, %seed.valid.1 ], [ %.35.1, %advance ]
  %.30.0 = phi i64 [ 0, %seed.valid.1 ], [ %.102, %advance ]
  %.26.0 = phi i64 [ %.28, %seed.valid.1 ], [ %.26.1, %advance ]
  %.38.0 = phi i64 [ 0, %seed.valid.1 ], [ %.256, %advance ]
  %.82 = icmp ugt i64 %.34.0, 0
  %.83 = and i1 true, %.82
  %.85 = icmp ugt i64 %.35.0, 0
  %.86 = and i1 %.83, %.85
  br i1 %.86, label %round.pop, label %finish

round.pop:                                        ; preds = %round.check
  %.89 = mul i64 0, %queue_capacity
  %.90 = add i64 %.89, %.30.0
  %.91 = mul i64 %.90, %walker_count
  %.92 = add i64 %.91, %index
  %.93 = getelementptr i64, ptr addrspace(1) %queue, i64 %.92
  %.94 = load i64, ptr addrspace(1) %.93, align 8
  %.95 = icmp sge i64 %.94, 0
  %.96 = icmp ult i64 %.94, %node_count
  %.97 = and i1 %.95, %.96
  br i1 %.97, label %current.valid, label %error.1

joint.match:                                      ; preds = %current.valid.1
  %.130 = getelementptr i64, ptr addrspace(1) %type_tags, i64 %.94
  %.131 = load i64, ptr addrspace(1) %.130, align 8
  %.132 = icmp eq i64 %.131, 1
  %.133 = and i1 true, %.132
  %.135 = getelementptr i64, ptr addrspace(1) %type_tags, i64 %.113
  %.136 = load i64, ptr addrspace(1) %.135, align 8
  %.137 = icmp eq i64 %.136, 1
  %.138 = and i1 %.133, %.137
  br i1 %.138, label %ability, label %advance

ability:                                          ; preds = %joint.match
  %.141 = getelementptr i64, ptr addrspace(1) %values, i64 %.94
  %.142 = load i64, ptr addrspace(1) %.141, align 8
  %.144 = getelementptr i64, ptr addrspace(1) %values, i64 %.113
  %.145 = load i64, ptr addrspace(1) %.144, align 8
  %.147 = call { i64, i1 } @llvm.smul.with.overflow.i64(i64 %.142, i64 %.145)
  %.148 = extractvalue { i64, i1 } %.147, 0
  %.149 = extractvalue { i64, i1 } %.147, 1
  br i1 %.149, label %error.3, label %int.ok

advance:                                          ; preds = %visit.end.1, %joint.match
  %.32.1 = phi i64 [ %.180, %visit.end.1 ], [ %.32.0, %joint.match ]
  %.33.1 = phi i64 [ %.229, %visit.end.1 ], [ %.33.0, %joint.match ]
  %.34.1 = phi i64 [ %.202, %visit.end.1 ], [ %.105, %joint.match ]
  %.35.1 = phi i64 [ %.251, %visit.end.1 ], [ %.124, %joint.match ]
  %.26.1 = phi i64 [ %.152, %visit.end.1 ], [ %.26.0, %joint.match ]
  %.256 = add i64 %.38.0, 1
  br label %round.check

finish:                                           ; preds = %round.check
  %.260 = getelementptr i64, ptr addrspace(1) %results, i64 %index
  store i64 %.26.0, ptr addrspace(1) %.260, align 8
  %.262 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 0, ptr addrspace(1) %.262, align 4
  br label %done

done:                                             ; preds = %error.7, %error.6, %error.5, %error.4, %error.3, %error.2, %error.1, %finish, %entry
  ret void

error.1:                                          ; preds = %edge.append.1, %edge.append, %current.valid, %round.pop
  %.265 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 1, ptr addrspace(1) %.265, align 4
  br label %done

error.2:                                          ; preds = %current.valid.1
  %.268 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 2, ptr addrspace(1) %.268, align 4
  br label %done

error.3:                                          ; preds = %int.ok, %ability
  %.271 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 3, ptr addrspace(1) %.271, align 4
  br label %done

error.4:                                          ; No predecessors!
  %.274 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 4, ptr addrspace(1) %.274, align 4
  br label %done

error.5:                                          ; preds = %visit.begin.1, %visit.begin
  %.277 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 5, ptr addrspace(1) %.277, align 4
  br label %done

error.6:                                          ; preds = %row.valid.1, %row.valid, %seed.valid, %start
  %.280 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 6, ptr addrspace(1) %.280, align 4
  br label %done

error.7:                                          ; No predecessors!
  %.283 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 7, ptr addrspace(1) %.283, align 4
  br label %done

seed.valid:                                       ; preds = %start
  %.50 = icmp eq i64 %.43, %queue_capacity
  %.51 = select i1 %.50, i64 0, i64 %.43
  %.53 = getelementptr i64, ptr addrspace(1) %heads, i64 %.41
  %.54 = load i64, ptr addrspace(1) %.53, align 8
  %.55 = mul i64 %queue_capacity, %walker_count
  %.56 = mul i64 0, %.55
  %.57 = add i64 %.56, %index
  %.58 = getelementptr i64, ptr addrspace(1) %queue, i64 %.57
  store i64 %.54, ptr addrspace(1) %.58, align 8
  %.60 = mul i64 1, %walker_count
  %.61 = add i64 %.60, %index
  %.62 = getelementptr i64, ptr addrspace(1) %seed_counts, i64 %.61
  %.63 = load i64, ptr addrspace(1) %.62, align 8
  %.64 = icmp ugt i64 %queue_capacity, 0
  %.65 = icmp ule i64 %.63, %queue_capacity
  %.66 = and i1 %.64, %.65
  br i1 %.66, label %seed.valid.1, label %error.6

seed.valid.1:                                     ; preds = %seed.valid
  %.70 = icmp eq i64 %.63, %queue_capacity
  %.71 = select i1 %.70, i64 0, i64 %.63
  %.73 = getelementptr i64, ptr addrspace(1) %heads, i64 %.61
  %.74 = load i64, ptr addrspace(1) %.73, align 8
  %.75 = mul i64 %queue_capacity, %walker_count
  %.76 = mul i64 1, %.75
  %.77 = add i64 %.76, %index
  %.78 = getelementptr i64, ptr addrspace(1) %queue, i64 %.77
  store i64 %.74, ptr addrspace(1) %.78, align 8
  br label %round.check

current.valid:                                    ; preds = %round.pop
  %.100 = add i64 %.30.0, 1
  %.101 = icmp eq i64 %.100, %queue_capacity
  %.102 = select i1 %.101, i64 0, i64 %.100
  %.105 = sub i64 %.34.0, 1
  %.108 = mul i64 1, %queue_capacity
  %.109 = add i64 %.108, %.31.0
  %.110 = mul i64 %.109, %walker_count
  %.111 = add i64 %.110, %index
  %.112 = getelementptr i64, ptr addrspace(1) %queue, i64 %.111
  %.113 = load i64, ptr addrspace(1) %.112, align 8
  %.114 = icmp sge i64 %.113, 0
  %.115 = icmp ult i64 %.113, %node_count
  %.116 = and i1 %.114, %.115
  br i1 %.116, label %current.valid.1, label %error.1

current.valid.1:                                  ; preds = %current.valid
  %.119 = add i64 %.31.0, 1
  %.120 = icmp eq i64 %.119, %queue_capacity
  %.121 = select i1 %.120, i64 0, i64 %.119
  %.124 = sub i64 %.35.0, 1
  %.127 = icmp ult i64 %.38.0, %max_visits
  br i1 %.127, label %joint.match, label %error.2

int.ok:                                           ; preds = %ability
  %.151 = call { i64, i1 } @llvm.sadd.with.overflow.i64(i64 %.26.0, i64 %.148)
  %.152 = extractvalue { i64, i1 } %.151, 0
  %.153 = extractvalue { i64, i1 } %.151, 1
  br i1 %.153, label %error.3, label %int.ok.1

int.ok.1:                                         ; preds = %int.ok
  br label %visit.begin

visit.begin:                                      ; preds = %int.ok.1
  %.157 = add i64 %node_count, 1
  %.158 = mul i64 0, %.157
  %.160 = add i64 %.158, %.94
  %.161 = getelementptr i64, ptr addrspace(1) %offsets, i64 %.160
  %.162 = load i64, ptr addrspace(1) %.161, align 8
  %.163 = add i64 %.160, 1
  %.164 = getelementptr i64, ptr addrspace(1) %offsets, i64 %.163
  %.165 = load i64, ptr addrspace(1) %.164, align 8
  %.166 = icmp sge i64 %.162, 0
  %.167 = icmp ule i64 %.162, %.165
  %.168 = icmp ule i64 %.165, %edge_count
  %.169 = and i1 %.167, %.168
  %.170 = and i1 %.166, %.169
  br i1 %.170, label %row.valid, label %error.5

visit.end:                                        ; preds = %edges.end
  br label %visit.begin.1

row.valid:                                        ; preds = %visit.begin
  %.172 = sub i64 %.165, %.162
  %.174 = sub i64 %queue_capacity, %.105
  %.175 = icmp ule i64 %.172, %.174
  br i1 %.175, label %queue.room, label %error.6

queue.room:                                       ; preds = %row.valid
  br label %edge.check

edge.check:                                       ; preds = %edge.store, %queue.room
  %.179 = phi i64 [ %.162, %queue.room ], [ %.198, %edge.store ]
  %.180 = phi i64 [ %.32.0, %queue.room ], [ %.197, %edge.store ]
  %.181 = icmp ult i64 %.179, %.165
  br i1 %.181, label %edge.append, label %edges.end

edge.append:                                      ; preds = %edge.check
  %.183 = getelementptr i64, ptr addrspace(1) %targets, i64 %.179
  %.184 = load i64, ptr addrspace(1) %.183, align 8
  %.185 = icmp sge i64 %.184, 0
  %.186 = icmp ult i64 %.184, %node_count
  %.187 = and i1 %.185, %.186
  br i1 %.187, label %edge.store, label %error.1

edge.store:                                       ; preds = %edge.append
  %.189 = mul i64 0, %queue_capacity
  %.190 = add i64 %.189, %.180
  %.191 = mul i64 %.190, %walker_count
  %.192 = add i64 %.191, %index
  %.193 = getelementptr i64, ptr addrspace(1) %queue, i64 %.192
  store i64 %.184, ptr addrspace(1) %.193, align 8
  %.195 = add i64 %.180, 1
  %.196 = icmp eq i64 %.195, %queue_capacity
  %.197 = select i1 %.196, i64 0, i64 %.195
  %.198 = add i64 %.179, 1
  br label %edge.check

edges.end:                                        ; preds = %edge.check
  %.202 = add i64 %.105, %.172
  br label %visit.end

visit.begin.1:                                    ; preds = %visit.end
  %.206 = add i64 %node_count, 1
  %.207 = mul i64 1, %.206
  %.209 = add i64 %.207, %.113
  %.210 = getelementptr i64, ptr addrspace(1) %offsets, i64 %.209
  %.211 = load i64, ptr addrspace(1) %.210, align 8
  %.212 = add i64 %.209, 1
  %.213 = getelementptr i64, ptr addrspace(1) %offsets, i64 %.212
  %.214 = load i64, ptr addrspace(1) %.213, align 8
  %.215 = icmp sge i64 %.211, 0
  %.216 = icmp ule i64 %.211, %.214
  %.217 = icmp ule i64 %.214, %edge_count
  %.218 = and i1 %.216, %.217
  %.219 = and i1 %.215, %.218
  br i1 %.219, label %row.valid.1, label %error.5

visit.end.1:                                      ; preds = %edges.end.1
  br label %advance

row.valid.1:                                      ; preds = %visit.begin.1
  %.221 = sub i64 %.214, %.211
  %.223 = sub i64 %queue_capacity, %.124
  %.224 = icmp ule i64 %.221, %.223
  br i1 %.224, label %queue.room.1, label %error.6

queue.room.1:                                     ; preds = %row.valid.1
  br label %edge.check.1

edge.check.1:                                     ; preds = %edge.store.1, %queue.room.1
  %.228 = phi i64 [ %.211, %queue.room.1 ], [ %.247, %edge.store.1 ]
  %.229 = phi i64 [ %.33.0, %queue.room.1 ], [ %.246, %edge.store.1 ]
  %.230 = icmp ult i64 %.228, %.214
  br i1 %.230, label %edge.append.1, label %edges.end.1

edge.append.1:                                    ; preds = %edge.check.1
  %.232 = getelementptr i64, ptr addrspace(1) %targets, i64 %.228
  %.233 = load i64, ptr addrspace(1) %.232, align 8
  %.234 = icmp sge i64 %.233, 0
  %.235 = icmp ult i64 %.233, %node_count
  %.236 = and i1 %.234, %.235
  br i1 %.236, label %edge.store.1, label %error.1

edge.store.1:                                     ; preds = %edge.append.1
  %.238 = mul i64 1, %queue_capacity
  %.239 = add i64 %.238, %.229
  %.240 = mul i64 %.239, %walker_count
  %.241 = add i64 %.240, %index
  %.242 = getelementptr i64, ptr addrspace(1) %queue, i64 %.241
  store i64 %.233, ptr addrspace(1) %.242, align 8
  %.244 = add i64 %.229, 1
  %.245 = icmp eq i64 %.244, %queue_capacity
  %.246 = select i1 %.245, i64 0, i64 %.244
  %.247 = add i64 %.228, 1
  br label %edge.check.1

edges.end.1:                                      ; preds = %edge.check.1
  %.251 = add i64 %.124, %.221
  br label %visit.end.1
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 0, 2147483647) i32 @llvm.nvvm.read.ptx.sreg.ctaid.x() #0

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 1, 1025) i32 @llvm.nvvm.read.ptx.sreg.ntid.x() #0

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 0, 1024) i32 @llvm.nvvm.read.ptx.sreg.tid.x() #0

; Function Attrs: nocallback nocreateundeforpoison nofree nosync nounwind speculatable willreturn memory(none)
declare { i64, i1 } @llvm.smul.with.overflow.i64(i64, i64) #1

; Function Attrs: nocallback nocreateundeforpoison nofree nosync nounwind speculatable willreturn memory(none)
declare { i64, i1 } @llvm.sadd.with.overflow.i64(i64, i64) #1

attributes #0 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #1 = { nocallback nocreateundeforpoison nofree nosync nounwind speculatable willreturn memory(none) }
