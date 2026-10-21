; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-p6:32:32-i64:64-i128:128-i256:256-v16:16-v32:32-n16:32:64"
target triple = "nvptx64-nvidia-cuda"

; Function Attrs: nofree norecurse nosync nounwind memory(argmem: readwrite)
define ptx_kernel void @jac_Dot_cursors_batch(ptr addrspace(1) readonly captures(none) %values, ptr addrspace(1) readonly captures(none) %type_tags, ptr addrspace(1) readonly captures(none) %offsets, ptr addrspace(1) readonly captures(none) %targets, ptr addrspace(1) readonly captures(none) %heads, ptr addrspace(1) readonly captures(none) %seed_counts, ptr addrspace(1) readonly captures(none) %initial_total, ptr addrspace(1) writeonly captures(none) %results, ptr addrspace(1) writeonly captures(none) %status, ptr addrspace(1) captures(none) %queue, i64 %node_count, i64 %edge_count, i64 %walker_count, i64 %queue_capacity, i64 %max_visits) local_unnamed_addr #0 {
entry:
  %.17 = tail call i32 @llvm.nvvm.read.ptx.sreg.ctaid.x()
  %.18 = zext nneg i32 %.17 to i64
  %.19 = tail call i32 @llvm.nvvm.read.ptx.sreg.ntid.x()
  %.20 = zext nneg i32 %.19 to i64
  %.21 = tail call i32 @llvm.nvvm.read.ptx.sreg.tid.x()
  %.22 = zext nneg i32 %.21 to i64
  %.23 = mul nuw nsw i64 %.18, %.20
  %index = add nuw nsw i64 %.23, %.22
  %.24 = icmp ult i64 %index, %walker_count
  br i1 %.24, label %start, label %done

start:                                            ; preds = %entry
  %.27 = getelementptr i64, ptr addrspace(1) %initial_total, i64 %index
  %.28 = load i64, ptr addrspace(1) %.27, align 8
  %.42 = getelementptr i64, ptr addrspace(1) %seed_counts, i64 %index
  %.43 = load i64, ptr addrspace(1) %.42, align 8
  %.44 = icmp ne i64 %queue_capacity, 0
  %.45 = icmp ule i64 %.43, %queue_capacity
  %.46 = and i1 %.44, %.45
  br i1 %.46, label %seed.valid, label %done.sink.split

round.pop:                                        ; preds = %round.pop.lr.ph, %advance
  %.2021891 = phi i64 [ %.43, %round.pop.lr.ph ], [ %.20219, %advance ]
  %.2512590 = phi i64 [ %.63, %round.pop.lr.ph ], [ %.25126, %advance ]
  %.1023389 = phi i64 [ 0, %round.pop.lr.ph ], [ %.102, %advance ]
  %.1214088 = phi i64 [ 0, %round.pop.lr.ph ], [ %.121, %advance ]
  %.1264786 = phi i64 [ 0, %round.pop.lr.ph ], [ %.256, %advance ]
  %.1525685 = phi i64 [ %.28, %round.pop.lr.ph ], [ %.15255, %advance ]
  %.180.lcssa6484 = phi i64 [ %.51, %round.pop.lr.ph ], [ %.180.lcssa63, %advance ]
  %.229.lcssa7283 = phi i64 [ %.71, %round.pop.lr.ph ], [ %.229.lcssa71, %advance ]
  %.91 = mul i64 %.1023389, %walker_count
  %gep15 = getelementptr i64, ptr addrspace(1) %.58, i64 %.91
  %.94 = load i64, ptr addrspace(1) %gep15, align 8
  %.95 = icmp sgt i64 %.94, -1
  %.96 = icmp ult i64 %.94, %node_count
  %.97 = and i1 %.95, %.96
  br i1 %.97, label %current.valid, label %done.sink.split

joint.match:                                      ; preds = %current.valid.1
  %.130 = getelementptr i64, ptr addrspace(1) %type_tags, i64 %.94
  %.131 = load i64, ptr addrspace(1) %.130, align 8
  %.132 = icmp eq i64 %.131, 1
  %.135 = getelementptr i64, ptr addrspace(1) %type_tags, i64 %.113
  %.136 = load i64, ptr addrspace(1) %.135, align 8
  %.137 = icmp eq i64 %.136, 1
  %.138 = and i1 %.132, %.137
  br i1 %.138, label %ability, label %advance

ability:                                          ; preds = %joint.match
  %.141 = getelementptr i64, ptr addrspace(1) %values, i64 %.94
  %.142 = load i64, ptr addrspace(1) %.141, align 8
  %.144 = getelementptr i64, ptr addrspace(1) %values, i64 %.113
  %.145 = load i64, ptr addrspace(1) %.144, align 8
  %.147 = tail call { i64, i1 } @llvm.smul.with.overflow.i64(i64 %.142, i64 %.145)
  %.149 = extractvalue { i64, i1 } %.147, 1
  br i1 %.149, label %done.sink.split, label %int.ok

advance:                                          ; preds = %edges.end.1, %joint.match
  %.229.lcssa71 = phi i64 [ %.229.lcssa, %edges.end.1 ], [ %.229.lcssa7283, %joint.match ]
  %.180.lcssa63 = phi i64 [ %.180.lcssa, %edges.end.1 ], [ %.180.lcssa6484, %joint.match ]
  %.15255 = phi i64 [ %.152, %edges.end.1 ], [ %.1525685, %joint.match ]
  %.25126 = phi i64 [ %.251, %edges.end.1 ], [ %.124, %joint.match ]
  %.20219 = phi i64 [ %.202, %edges.end.1 ], [ %.105, %joint.match ]
  %.256 = add i64 %.1264786, 1
  %.82 = icmp ne i64 %.20219, 0
  %.85 = icmp ne i64 %.25126, 0
  %.86 = and i1 %.82, %.85
  br i1 %.86, label %round.pop, label %finish

finish:                                           ; preds = %advance, %seed.valid.1
  %.15256.lcssa = phi i64 [ %.28, %seed.valid.1 ], [ %.15255, %advance ]
  %.260 = getelementptr i64, ptr addrspace(1) %results, i64 %index
  store i64 %.15256.lcssa, ptr addrspace(1) %.260, align 8
  br label %done.sink.split

done.sink.split:                                  ; preds = %row.valid, %row.valid.1, %int.ok.1, %edges.end, %ability, %int.ok, %current.valid.1, %round.pop, %current.valid, %edge.append, %edge.append.1, %start, %seed.valid, %finish
  %.sink = phi i32 [ 6, %seed.valid ], [ 1, %edge.append.1 ], [ 1, %edge.append ], [ 6, %start ], [ 0, %finish ], [ 3, %ability ], [ 2, %current.valid.1 ], [ 1, %current.valid ], [ 1, %round.pop ], [ 3, %int.ok ], [ 5, %edges.end ], [ 6, %row.valid.1 ], [ 6, %row.valid ], [ 5, %int.ok.1 ]
  %.280 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 %.sink, ptr addrspace(1) %.280, align 4
  br label %done

done:                                             ; preds = %done.sink.split, %entry
  ret void

seed.valid:                                       ; preds = %start
  %.50 = icmp eq i64 %.43, %queue_capacity
  %.51 = select i1 %.50, i64 0, i64 %.43
  %.53 = getelementptr i64, ptr addrspace(1) %heads, i64 %index
  %.54 = load i64, ptr addrspace(1) %.53, align 8
  %.58 = getelementptr i64, ptr addrspace(1) %queue, i64 %index
  store i64 %.54, ptr addrspace(1) %.58, align 8
  %.61 = add i64 %walker_count, %index
  %.62 = getelementptr i64, ptr addrspace(1) %seed_counts, i64 %.61
  %.63 = load i64, ptr addrspace(1) %.62, align 8
  %.65.not = icmp ugt i64 %.63, %queue_capacity
  br i1 %.65.not, label %done.sink.split, label %seed.valid.1

seed.valid.1:                                     ; preds = %seed.valid
  %.55 = mul i64 %queue_capacity, %walker_count
  %.73 = getelementptr i64, ptr addrspace(1) %heads, i64 %.61
  %.74 = load i64, ptr addrspace(1) %.73, align 8
  %0 = getelementptr i64, ptr addrspace(1) %queue, i64 %.55
  %.78 = getelementptr i64, ptr addrspace(1) %0, i64 %index
  store i64 %.74, ptr addrspace(1) %.78, align 8
  %.8280 = icmp ne i64 %.43, 0
  %.8581 = icmp ne i64 %.63, 0
  %.8682 = and i1 %.8280, %.8581
  br i1 %.8682, label %round.pop.lr.ph, label %finish

round.pop.lr.ph:                                  ; preds = %seed.valid.1
  %.70 = icmp eq i64 %.63, %queue_capacity
  %.71 = select i1 %.70, i64 0, i64 %.63
  %1 = getelementptr i64, ptr addrspace(1) %offsets, i64 %node_count
  %2 = getelementptr i8, ptr addrspace(1) %1, i64 8
  br label %round.pop

current.valid:                                    ; preds = %round.pop
  %.100 = add i64 %.1023389, 1
  %.101 = icmp eq i64 %.100, %queue_capacity
  %.102 = select i1 %.101, i64 0, i64 %.100
  %.105 = add i64 %.2021891, -1
  %.109 = add i64 %.1214088, %queue_capacity
  %.110 = mul i64 %.109, %walker_count
  %gep17 = getelementptr i64, ptr addrspace(1) %.58, i64 %.110
  %.113 = load i64, ptr addrspace(1) %gep17, align 8
  %.114 = icmp sgt i64 %.113, -1
  %.115 = icmp ult i64 %.113, %node_count
  %.116 = and i1 %.114, %.115
  br i1 %.116, label %current.valid.1, label %done.sink.split

current.valid.1:                                  ; preds = %current.valid
  %.119 = add i64 %.1214088, 1
  %.120 = icmp eq i64 %.119, %queue_capacity
  %.121 = select i1 %.120, i64 0, i64 %.119
  %.124 = add i64 %.2512590, -1
  %.127 = icmp ult i64 %.1264786, %max_visits
  br i1 %.127, label %joint.match, label %done.sink.split

int.ok:                                           ; preds = %ability
  %.148 = extractvalue { i64, i1 } %.147, 0
  %.151 = tail call { i64, i1 } @llvm.sadd.with.overflow.i64(i64 %.1525685, i64 %.148)
  %.153 = extractvalue { i64, i1 } %.151, 1
  br i1 %.153, label %done.sink.split, label %int.ok.1

int.ok.1:                                         ; preds = %int.ok
  %.152 = extractvalue { i64, i1 } %.151, 0
  %.161 = getelementptr i64, ptr addrspace(1) %offsets, i64 %.94
  %.162 = load i64, ptr addrspace(1) %.161, align 8
  %.164 = getelementptr i8, ptr addrspace(1) %.161, i64 8
  %.165 = load i64, ptr addrspace(1) %.164, align 8
  %.166 = icmp sgt i64 %.162, -1
  %.167 = icmp ule i64 %.162, %.165
  %.168 = icmp ule i64 %.165, %edge_count
  %.169 = and i1 %.167, %.168
  %.170 = and i1 %.166, %.169
  br i1 %.170, label %row.valid, label %done.sink.split

row.valid:                                        ; preds = %int.ok.1
  %.172 = sub nuw i64 %.165, %.162
  %.174 = sub i64 %queue_capacity, %.105
  %.175.not = icmp ugt i64 %.172, %.174
  br i1 %.175.not, label %done.sink.split, label %queue.room

queue.room:                                       ; preds = %row.valid
  %.1815 = icmp ult i64 %.162, %.165
  br i1 %.1815, label %edge.append, label %edges.end

edge.append:                                      ; preds = %queue.room, %edge.store
  %.1807 = phi i64 [ %.197, %edge.store ], [ %.180.lcssa6484, %queue.room ]
  %.1796 = phi i64 [ %.198, %edge.store ], [ %.162, %queue.room ]
  %.183 = getelementptr i64, ptr addrspace(1) %targets, i64 %.1796
  %.184 = load i64, ptr addrspace(1) %.183, align 8
  %.185 = icmp sgt i64 %.184, -1
  %.186 = icmp ult i64 %.184, %node_count
  %.187 = and i1 %.185, %.186
  br i1 %.187, label %edge.store, label %done.sink.split

edge.store:                                       ; preds = %edge.append
  %.191 = mul i64 %.1807, %walker_count
  %gep = getelementptr i64, ptr addrspace(1) %.58, i64 %.191
  store i64 %.184, ptr addrspace(1) %gep, align 8
  %.195 = add i64 %.1807, 1
  %.196 = icmp eq i64 %.195, %queue_capacity
  %.197 = select i1 %.196, i64 0, i64 %.195
  %.198 = add nuw i64 %.1796, 1
  %.181 = icmp ult i64 %.198, %.165
  br i1 %.181, label %edge.append, label %edges.end

edges.end:                                        ; preds = %edge.store, %queue.room
  %.180.lcssa = phi i64 [ %.180.lcssa6484, %queue.room ], [ %.197, %edge.store ]
  %.202 = add i64 %.172, %.105
  %.210 = getelementptr i64, ptr addrspace(1) %2, i64 %.113
  %.211 = load i64, ptr addrspace(1) %.210, align 8
  %.213 = getelementptr i8, ptr addrspace(1) %.210, i64 8
  %.214 = load i64, ptr addrspace(1) %.213, align 8
  %.215 = icmp sgt i64 %.211, -1
  %.216 = icmp ule i64 %.211, %.214
  %.217 = icmp ule i64 %.214, %edge_count
  %.218 = and i1 %.216, %.217
  %.219 = and i1 %.215, %.218
  br i1 %.219, label %row.valid.1, label %done.sink.split

row.valid.1:                                      ; preds = %edges.end
  %.221 = sub nuw i64 %.214, %.211
  %.223 = sub i64 %queue_capacity, %.124
  %.224.not = icmp ugt i64 %.221, %.223
  br i1 %.224.not, label %done.sink.split, label %queue.room.1

queue.room.1:                                     ; preds = %row.valid.1
  %.23010 = icmp ult i64 %.211, %.214
  br i1 %.23010, label %edge.append.1, label %edges.end.1

edge.append.1:                                    ; preds = %queue.room.1, %edge.store.1
  %.22912 = phi i64 [ %.246, %edge.store.1 ], [ %.229.lcssa7283, %queue.room.1 ]
  %.22811 = phi i64 [ %.247, %edge.store.1 ], [ %.211, %queue.room.1 ]
  %.232 = getelementptr i64, ptr addrspace(1) %targets, i64 %.22811
  %.233 = load i64, ptr addrspace(1) %.232, align 8
  %.234 = icmp sgt i64 %.233, -1
  %.235 = icmp ult i64 %.233, %node_count
  %.236 = and i1 %.234, %.235
  br i1 %.236, label %edge.store.1, label %done.sink.split

edge.store.1:                                     ; preds = %edge.append.1
  %.239 = add i64 %.22912, %queue_capacity
  %.240 = mul i64 %.239, %walker_count
  %gep9 = getelementptr i64, ptr addrspace(1) %.58, i64 %.240
  store i64 %.233, ptr addrspace(1) %gep9, align 8
  %.244 = add i64 %.22912, 1
  %.245 = icmp eq i64 %.244, %queue_capacity
  %.246 = select i1 %.245, i64 0, i64 %.244
  %.247 = add nuw i64 %.22811, 1
  %.230 = icmp ult i64 %.247, %.214
  br i1 %.230, label %edge.append.1, label %edges.end.1

edges.end.1:                                      ; preds = %edge.store.1, %queue.room.1
  %.229.lcssa = phi i64 [ %.229.lcssa7283, %queue.room.1 ], [ %.246, %edge.store.1 ]
  %.251 = add i64 %.221, %.124
  br label %advance
}

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 0, 2147483647) i32 @llvm.nvvm.read.ptx.sreg.ctaid.x() #1

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 1, 1025) i32 @llvm.nvvm.read.ptx.sreg.ntid.x() #1

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 0, 1024) i32 @llvm.nvvm.read.ptx.sreg.tid.x() #1

; Function Attrs: mustprogress nocallback nocreateundeforpoison nofree nosync nounwind speculatable willreturn memory(none)
declare { i64, i1 } @llvm.smul.with.overflow.i64(i64, i64) #2

; Function Attrs: mustprogress nocallback nocreateundeforpoison nofree nosync nounwind speculatable willreturn memory(none)
declare { i64, i1 } @llvm.sadd.with.overflow.i64(i64, i64) #2

attributes #0 = { nofree norecurse nosync nounwind memory(argmem: readwrite) }
attributes #1 = { mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #2 = { mustprogress nocallback nocreateundeforpoison nofree nosync nounwind speculatable willreturn memory(none) }
