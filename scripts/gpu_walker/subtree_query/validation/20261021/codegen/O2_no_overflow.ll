; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-p6:32:32-i64:64-i128:128-i256:256-v16:16-v32:32-n16:32:64"
target triple = "nvptx64-nvidia-cuda"

; Function Attrs: nofree norecurse nosync nounwind memory(argmem: readwrite)
define ptx_kernel void @jac_SubtreeQuery_csr_batch(ptr addrspace(1) readonly captures(none) %values, ptr addrspace(1) readonly captures(none) %values_1, ptr addrspace(1) readonly captures(none) %offsets, ptr addrspace(1) readonly captures(none) %targets, ptr addrspace(1) readonly captures(none) %heads, ptr addrspace(1) readonly captures(none) %initial_total, ptr addrspace(1) readonly captures(none) %initial_1, ptr addrspace(1) readonly captures(none) %initial_2, ptr addrspace(1) readonly captures(none) %initial_3, ptr addrspace(1) readonly captures(none) %initial_4, ptr addrspace(1) writeonly captures(none) %results, ptr addrspace(1) writeonly captures(none) %results_1, ptr addrspace(1) writeonly captures(none) %results_2, ptr addrspace(1) writeonly captures(none) %results_3, ptr addrspace(1) writeonly captures(none) %results_4, ptr addrspace(1) writeonly captures(none) %status, ptr addrspace(1) captures(none) %queue, i64 %node_count, i64 %edge_count, i64 %walker_count, i64 %queue_capacity, i64 %max_visits) local_unnamed_addr #0 {
entry:
  %.24 = tail call i32 @llvm.nvvm.read.ptx.sreg.ctaid.x()
  %.25 = zext nneg i32 %.24 to i64
  %.26 = tail call i32 @llvm.nvvm.read.ptx.sreg.ntid.x()
  %.27 = zext nneg i32 %.26 to i64
  %.28 = tail call i32 @llvm.nvvm.read.ptx.sreg.tid.x()
  %.29 = zext nneg i32 %.28 to i64
  %.30 = mul nuw nsw i64 %.25, %.27
  %index = add nuw nsw i64 %.30, %.29
  %.31 = icmp ult i64 %index, %walker_count
  br i1 %.31, label %start, label %done

start:                                            ; preds = %entry
  %.33 = getelementptr i64, ptr addrspace(1) %heads, i64 %index
  %.34 = load i64, ptr addrspace(1) %.33, align 8
  %.35 = getelementptr i64, ptr addrspace(1) %initial_total, i64 %index
  %.36 = load i64, ptr addrspace(1) %.35, align 8
  %.37 = getelementptr i64, ptr addrspace(1) %initial_1, i64 %index
  %.38 = load i64, ptr addrspace(1) %.37, align 8
  %.39 = getelementptr i64, ptr addrspace(1) %initial_2, i64 %index
  %.40 = load i64, ptr addrspace(1) %.39, align 8
  %.41 = icmp ne i64 %.40, 0
  %.42 = getelementptr i64, ptr addrspace(1) %initial_3, i64 %index
  %.43 = load i64, ptr addrspace(1) %.42, align 8
  %.44 = getelementptr i64, ptr addrspace(1) %initial_4, i64 %index
  %.45 = load i64, ptr addrspace(1) %.44, align 8
  %.46 = icmp eq i64 %.34, -1
  br i1 %.46, label %finish, label %queue.init

queue.init:                                       ; preds = %start
  %.48.not = icmp eq i64 %queue_capacity, 0
  br i1 %.48.not, label %done.sink.split, label %queue.ready

queue.ready:                                      ; preds = %queue.init
  %.50 = getelementptr i64, ptr addrspace(1) %queue, i64 %index
  store i64 %.34, ptr addrspace(1) %.50, align 8
  %.52 = icmp ne i64 %queue_capacity, 1
  %.53 = zext i1 %.52 to i64
  br label %queue.pop

queue.pop:                                        ; preds = %queue.ready, %advance
  %visited35 = phi i64 [ %.43, %queue.ready ], [ %.77, %advance ]
  %has_alert34 = phi i1 [ %.41, %queue.ready ], [ %.97, %advance ]
  %total33 = phi i64 [ %.38, %queue.ready ], [ %.96, %advance ]
  %count32 = phi i64 [ %.36, %queue.ready ], [ %.95, %advance ]
  %steps31 = phi i64 [ 0, %queue.ready ], [ %.133, %advance ]
  %pending30 = phi i64 [ 1, %queue.ready ], [ %.132, %advance ]
  %write.pos29 = phi i64 [ %.53, %queue.ready ], [ %tail.lcssa, %advance ]
  %read.pos28 = phi i64 [ 0, %queue.ready ], [ %.63, %advance ]
  %.57 = mul i64 %read.pos28, %walker_count
  %gep27 = getelementptr i64, ptr addrspace(1) %.50, i64 %.57
  %.60 = load i64, ptr addrspace(1) %gep27, align 8
  %.61 = add i64 %read.pos28, 1
  %.62 = icmp eq i64 %.61, %queue_capacity
  %.63 = select i1 %.62, i64 0, i64 %.61
  %.64 = add i64 %pending30, -1
  %.65 = icmp sgt i64 %.60, -1
  %.66 = icmp ult i64 %.60, %node_count
  %.67 = and i1 %.65, %.66
  br i1 %.67, label %visit.limit, label %done.sink.split

visit.limit:                                      ; preds = %queue.pop
  %exitcond.not = icmp eq i64 %steps31, %max_visits
  br i1 %exitcond.not, label %done.sink.split, label %ability

ability:                                          ; preds = %visit.limit
  %.71 = getelementptr i64, ptr addrspace(1) %values, i64 %.60
  %.72 = load i64, ptr addrspace(1) %.71, align 8
  %.77 = add i64 %visited35, 1
  %.80.not = icmp slt i64 %.72, %.45
  br i1 %.80.not, label %update.end, label %update.then

queue.room:                                       ; preds = %update.end
  %.111 = sub nuw i64 %.104, %.101
  %.112 = sub i64 %queue_capacity, %.64
  %.113.not = icmp ugt i64 %.111, %.112
  br i1 %.113.not, label %done.sink.split, label %edges.check.preheader

edges.check.preheader:                            ; preds = %queue.room
  %.11523 = icmp ult i64 %.101, %.104
  br i1 %.11523, label %edge.read, label %advance

edge.read:                                        ; preds = %edges.check.preheader, %queue.append
  %tail25 = phi i64 [ %.129, %queue.append ], [ %write.pos29, %edges.check.preheader ]
  %edge24 = phi i64 [ %.130, %queue.append ], [ %.101, %edges.check.preheader ]
  %.117 = getelementptr i64, ptr addrspace(1) %targets, i64 %edge24
  %.118 = load i64, ptr addrspace(1) %.117, align 8
  %.119 = icmp sgt i64 %.118, -1
  %.120 = icmp ult i64 %.118, %node_count
  %.121 = and i1 %.119, %.120
  br i1 %.121, label %queue.append, label %done.sink.split

queue.append:                                     ; preds = %edge.read
  %.123 = mul i64 %tail25, %walker_count
  %gep = getelementptr i64, ptr addrspace(1) %.50, i64 %.123
  store i64 %.118, ptr addrspace(1) %gep, align 8
  %.127 = add i64 %tail25, 1
  %.128 = icmp eq i64 %.127, %queue_capacity
  %.129 = select i1 %.128, i64 0, i64 %.127
  %.130 = add nuw i64 %edge24, 1
  %.115 = icmp ult i64 %.130, %.104
  br i1 %.115, label %edge.read, label %advance

advance:                                          ; preds = %queue.append, %edges.check.preheader
  %tail.lcssa = phi i64 [ %write.pos29, %edges.check.preheader ], [ %.129, %queue.append ]
  %.132 = add i64 %.111, %.64
  %.133 = add i64 %steps31, 1
  %.55 = icmp eq i64 %.132, 0
  br i1 %.55, label %finish, label %queue.pop

finish:                                           ; preds = %advance, %start
  %.135 = phi i64 [ %.36, %start ], [ %.95, %advance ]
  %.136 = phi i64 [ %.38, %start ], [ %.96, %advance ]
  %.137 = phi i1 [ %.41, %start ], [ %.97, %advance ]
  %.138 = phi i64 [ %.43, %start ], [ %.77, %advance ]
  %.140 = getelementptr i64, ptr addrspace(1) %results, i64 %index
  store i64 %.135, ptr addrspace(1) %.140, align 8
  %.142 = getelementptr i64, ptr addrspace(1) %results_1, i64 %index
  store i64 %.136, ptr addrspace(1) %.142, align 8
  %.144 = zext i1 %.137 to i64
  %.145 = getelementptr i64, ptr addrspace(1) %results_2, i64 %index
  store i64 %.144, ptr addrspace(1) %.145, align 8
  %.147 = getelementptr i64, ptr addrspace(1) %results_3, i64 %index
  store i64 %.138, ptr addrspace(1) %.147, align 8
  %.149 = getelementptr i64, ptr addrspace(1) %results_4, i64 %index
  store i64 %.45, ptr addrspace(1) %.149, align 8
  br label %done.sink.split

done.sink.split:                                  ; preds = %queue.room, %update.end, %visit.limit, %queue.pop, %edge.read, %queue.init, %finish
  %.sink = phi i32 [ 0, %finish ], [ 1, %edge.read ], [ 6, %queue.init ], [ 2, %visit.limit ], [ 1, %queue.pop ], [ 6, %queue.room ], [ 5, %update.end ]
  %.169 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 %.sink, ptr addrspace(1) %.169, align 4
  br label %done

done:                                             ; preds = %done.sink.split, %entry
  ret void

update.then:                                      ; preds = %ability
  %.87 = add i64 %.72, %total33
  %.83 = add i64 %count32, 1
  %.73 = getelementptr i64, ptr addrspace(1) %values_1, i64 %.60
  %.74 = load i64, ptr addrspace(1) %.73, align 8
  %.75 = icmp ne i64 %.74, 0
  %.92 = select i1 %has_alert34, i1 true, i1 %.75
  br label %update.end

update.end:                                       ; preds = %ability, %update.then
  %.95 = phi i64 [ %.83, %update.then ], [ %count32, %ability ]
  %.96 = phi i64 [ %.87, %update.then ], [ %total33, %ability ]
  %.97 = phi i1 [ %.92, %update.then ], [ %has_alert34, %ability ]
  %.100 = getelementptr i64, ptr addrspace(1) %offsets, i64 %.60
  %.101 = load i64, ptr addrspace(1) %.100, align 8
  %.103 = getelementptr i8, ptr addrspace(1) %.100, i64 8
  %.104 = load i64, ptr addrspace(1) %.103, align 8
  %.105 = icmp sgt i64 %.101, -1
  %.106 = icmp ule i64 %.101, %.104
  %.107 = icmp ule i64 %.104, %edge_count
  %.108 = and i1 %.106, %.107
  %.109 = and i1 %.105, %.108
  br i1 %.109, label %queue.room, label %done.sink.split
}

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 0, 2147483647) i32 @llvm.nvvm.read.ptx.sreg.ctaid.x() #1

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 1, 1025) i32 @llvm.nvvm.read.ptx.sreg.ntid.x() #1

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 0, 1024) i32 @llvm.nvvm.read.ptx.sreg.tid.x() #1

attributes #0 = { nofree norecurse nosync nounwind memory(argmem: readwrite) }
attributes #1 = { mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none) }
