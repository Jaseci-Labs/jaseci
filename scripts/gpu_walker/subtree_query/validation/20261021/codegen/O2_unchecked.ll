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
  %.50 = getelementptr i64, ptr addrspace(1) %queue, i64 %index
  store i64 %.34, ptr addrspace(1) %.50, align 8
  %.52 = icmp ne i64 %queue_capacity, 1
  %.53 = zext i1 %.52 to i64
  br label %queue.pop

queue.pop:                                        ; preds = %queue.init, %advance
  %visited12 = phi i64 [ %.43, %queue.init ], [ %.77, %advance ]
  %has_alert11 = phi i1 [ %.41, %queue.init ], [ %.97, %advance ]
  %total10 = phi i64 [ %.38, %queue.init ], [ %.96, %advance ]
  %count9 = phi i64 [ %.36, %queue.init ], [ %.95, %advance ]
  %pending8 = phi i64 [ 1, %queue.init ], [ %.132, %advance ]
  %write.pos7 = phi i64 [ %.53, %queue.init ], [ %tail.lcssa, %advance ]
  %read.pos6 = phi i64 [ 0, %queue.init ], [ %.63, %advance ]
  %.57 = mul i64 %read.pos6, %walker_count
  %gep5 = getelementptr i64, ptr addrspace(1) %.50, i64 %.57
  %.60 = load i64, ptr addrspace(1) %gep5, align 8
  %.61 = add i64 %read.pos6, 1
  %.62 = icmp eq i64 %.61, %queue_capacity
  %.63 = select i1 %.62, i64 0, i64 %.61
  %.71 = getelementptr i64, ptr addrspace(1) %values, i64 %.60
  %.72 = load i64, ptr addrspace(1) %.71, align 8
  %.77 = add i64 %visited12, 1
  %.80.not = icmp slt i64 %.72, %.45
  br i1 %.80.not, label %update.end, label %update.then

edge.read:                                        ; preds = %edge.read.prol.loopexit, %edge.read
  %tail3 = phi i64 [ %.129.1, %edge.read ], [ %tail3.unr, %edge.read.prol.loopexit ]
  %edge2 = phi i64 [ %.130.1, %edge.read ], [ %edge2.unr, %edge.read.prol.loopexit ]
  %.117 = getelementptr i64, ptr addrspace(1) %targets, i64 %edge2
  %.118 = load i64, ptr addrspace(1) %.117, align 8
  %.123 = mul i64 %tail3, %walker_count
  %gep = getelementptr i64, ptr addrspace(1) %.50, i64 %.123
  store i64 %.118, ptr addrspace(1) %gep, align 8
  %.127 = add i64 %tail3, 1
  %.128 = icmp eq i64 %.127, %queue_capacity
  %.129 = select i1 %.128, i64 0, i64 %.127
  %0 = getelementptr i64, ptr addrspace(1) %targets, i64 %edge2
  %.117.1 = getelementptr i8, ptr addrspace(1) %0, i64 8
  %.118.1 = load i64, ptr addrspace(1) %.117.1, align 8
  %.123.1 = mul i64 %.129, %walker_count
  %gep.1 = getelementptr i64, ptr addrspace(1) %.50, i64 %.123.1
  store i64 %.118.1, ptr addrspace(1) %gep.1, align 8
  %.127.1 = add i64 %.129, 1
  %.128.1 = icmp eq i64 %.127.1, %queue_capacity
  %.129.1 = select i1 %.128.1, i64 0, i64 %.127.1
  %.130.1 = add nuw i64 %edge2, 2
  %.115.1 = icmp ult i64 %.130.1, %.104
  br i1 %.115.1, label %edge.read, label %advance

advance:                                          ; preds = %edge.read.prol.loopexit, %edge.read, %update.end
  %tail.lcssa = phi i64 [ %write.pos7, %update.end ], [ %.129.lcssa.unr, %edge.read.prol.loopexit ], [ %.129.1, %edge.read ]
  %1 = xor i64 %.101, -1
  %.64 = add i64 %pending8, %1
  %.132 = add i64 %.64, %.104
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
  %.151 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 0, ptr addrspace(1) %.151, align 4
  br label %done

done:                                             ; preds = %finish, %entry
  ret void

update.then:                                      ; preds = %queue.pop
  %.87 = add i64 %.72, %total10
  %.83 = add i64 %count9, 1
  %.73 = getelementptr i64, ptr addrspace(1) %values_1, i64 %.60
  %.74 = load i64, ptr addrspace(1) %.73, align 8
  %.75 = icmp ne i64 %.74, 0
  %.92 = select i1 %has_alert11, i1 true, i1 %.75
  br label %update.end

update.end:                                       ; preds = %queue.pop, %update.then
  %.95 = phi i64 [ %.83, %update.then ], [ %count9, %queue.pop ]
  %.96 = phi i64 [ %.87, %update.then ], [ %total10, %queue.pop ]
  %.97 = phi i1 [ %.92, %update.then ], [ %has_alert11, %queue.pop ]
  %.100 = getelementptr i64, ptr addrspace(1) %offsets, i64 %.60
  %.101 = load i64, ptr addrspace(1) %.100, align 8
  %.103 = getelementptr i8, ptr addrspace(1) %.100, i64 8
  %.104 = load i64, ptr addrspace(1) %.103, align 8
  %.1151 = icmp ult i64 %.101, %.104
  br i1 %.1151, label %edge.read.preheader, label %advance

edge.read.preheader:                              ; preds = %update.end
  %2 = sub nuw i64 %.104, %.101
  %.neg = add i64 %.101, 1
  %xtraiter = and i64 %2, 1
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br i1 %lcmp.mod.not, label %edge.read.prol.loopexit, label %edge.read.prol

edge.read.prol:                                   ; preds = %edge.read.preheader
  %.117.prol = getelementptr i64, ptr addrspace(1) %targets, i64 %.101
  %.118.prol = load i64, ptr addrspace(1) %.117.prol, align 8
  %.123.prol = mul i64 %write.pos7, %walker_count
  %gep.prol = getelementptr i64, ptr addrspace(1) %.50, i64 %.123.prol
  store i64 %.118.prol, ptr addrspace(1) %gep.prol, align 8
  %.127.prol = add i64 %write.pos7, 1
  %.128.prol = icmp eq i64 %.127.prol, %queue_capacity
  %.129.prol = select i1 %.128.prol, i64 0, i64 %.127.prol
  %.130.prol = add nuw i64 %.101, 1
  br label %edge.read.prol.loopexit

edge.read.prol.loopexit:                          ; preds = %edge.read.prol, %edge.read.preheader
  %tail3.unr = phi i64 [ %write.pos7, %edge.read.preheader ], [ %.129.prol, %edge.read.prol ]
  %edge2.unr = phi i64 [ %.101, %edge.read.preheader ], [ %.130.prol, %edge.read.prol ]
  %.129.lcssa.unr = phi i64 [ poison, %edge.read.preheader ], [ %.129.prol, %edge.read.prol ]
  %3 = icmp eq i64 %.104, %.neg
  br i1 %3, label %advance, label %edge.read
}

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 0, 2147483647) i32 @llvm.nvvm.read.ptx.sreg.ctaid.x() #1

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 1, 1025) i32 @llvm.nvvm.read.ptx.sreg.ntid.x() #1

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 0, 1024) i32 @llvm.nvvm.read.ptx.sreg.tid.x() #1

attributes #0 = { nofree norecurse nosync nounwind memory(argmem: readwrite) }
attributes #1 = { mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none) }
