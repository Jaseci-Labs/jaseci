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
  %.53 = getelementptr i64, ptr addrspace(1) %heads, i64 %index
  %.54 = load i64, ptr addrspace(1) %.53, align 8
  %.55 = mul i64 %queue_capacity, %walker_count
  %.58 = getelementptr i64, ptr addrspace(1) %queue, i64 %index
  store i64 %.54, ptr addrspace(1) %.58, align 8
  %.61 = add i64 %walker_count, %index
  %.62 = getelementptr i64, ptr addrspace(1) %seed_counts, i64 %.61
  %.63 = load i64, ptr addrspace(1) %.62, align 8
  %.73 = getelementptr i64, ptr addrspace(1) %heads, i64 %.61
  %.74 = load i64, ptr addrspace(1) %.73, align 8
  %0 = getelementptr i64, ptr addrspace(1) %queue, i64 %.55
  %.78 = getelementptr i64, ptr addrspace(1) %0, i64 %index
  store i64 %.74, ptr addrspace(1) %.78, align 8
  %.8227 = icmp ne i64 %.43, 0
  %.8528 = icmp ne i64 %.63, 0
  %.8629 = and i1 %.8227, %.8528
  br i1 %.8629, label %round.pop.lr.ph, label %finish

round.pop.lr.ph:                                  ; preds = %start
  %.70 = icmp eq i64 %.63, %queue_capacity
  %.71 = select i1 %.70, i64 0, i64 %.63
  %.50 = icmp eq i64 %.43, %queue_capacity
  %.51 = select i1 %.50, i64 0, i64 %.43
  %1 = getelementptr i64, ptr addrspace(1) %offsets, i64 %node_count
  %2 = getelementptr i8, ptr addrspace(1) %1, i64 8
  br label %round.pop

round.pop:                                        ; preds = %round.pop.lr.ph, %advance
  %.2021437 = phi i64 [ %.43, %round.pop.lr.ph ], [ %.20215, %advance ]
  %.2511636 = phi i64 [ %.63, %round.pop.lr.ph ], [ %.25117, %advance ]
  %.1021835 = phi i64 [ 0, %round.pop.lr.ph ], [ %.102, %advance ]
  %.1211934 = phi i64 [ 0, %round.pop.lr.ph ], [ %.121, %advance ]
  %.1522133 = phi i64 [ %.28, %round.pop.lr.ph ], [ %.15220, %advance ]
  %.180.lcssa2332 = phi i64 [ %.51, %round.pop.lr.ph ], [ %.180.lcssa22, %advance ]
  %.229.lcssa2531 = phi i64 [ %.71, %round.pop.lr.ph ], [ %.229.lcssa24, %advance ]
  %.91 = mul i64 %.1021835, %walker_count
  %gep11 = getelementptr i64, ptr addrspace(1) %.58, i64 %.91
  %.94 = load i64, ptr addrspace(1) %gep11, align 8
  %.100 = add i64 %.1021835, 1
  %.101 = icmp eq i64 %.100, %queue_capacity
  %.102 = select i1 %.101, i64 0, i64 %.100
  %.105 = add i64 %.2021437, -1
  %.109 = add i64 %.1211934, %queue_capacity
  %.110 = mul i64 %.109, %walker_count
  %gep13 = getelementptr i64, ptr addrspace(1) %.58, i64 %.110
  %.113 = load i64, ptr addrspace(1) %gep13, align 8
  %.119 = add i64 %.1211934, 1
  %.120 = icmp eq i64 %.119, %queue_capacity
  %.121 = select i1 %.120, i64 0, i64 %.119
  %.124 = add i64 %.2511636, -1
  %.130 = getelementptr i64, ptr addrspace(1) %type_tags, i64 %.94
  %.131 = load i64, ptr addrspace(1) %.130, align 8
  %.132 = icmp eq i64 %.131, 1
  %.135 = getelementptr i64, ptr addrspace(1) %type_tags, i64 %.113
  %.136 = load i64, ptr addrspace(1) %.135, align 8
  %.137 = icmp eq i64 %.136, 1
  %.138 = and i1 %.132, %.137
  br i1 %.138, label %ability, label %advance

ability:                                          ; preds = %round.pop
  %.141 = getelementptr i64, ptr addrspace(1) %values, i64 %.94
  %.142 = load i64, ptr addrspace(1) %.141, align 8
  %.144 = getelementptr i64, ptr addrspace(1) %values, i64 %.113
  %.145 = load i64, ptr addrspace(1) %.144, align 8
  %.148 = mul i64 %.145, %.142
  %.152 = add i64 %.1522133, %.148
  %.161 = getelementptr i64, ptr addrspace(1) %offsets, i64 %.94
  %.162 = load i64, ptr addrspace(1) %.161, align 8
  %.164 = getelementptr i8, ptr addrspace(1) %.161, i64 8
  %.165 = load i64, ptr addrspace(1) %.164, align 8
  %.1811 = icmp ult i64 %.162, %.165
  br i1 %.1811, label %edge.append.preheader, label %edges.end

edge.append.preheader:                            ; preds = %ability
  %3 = sub nuw i64 %.165, %.162
  %.neg = add i64 %.162, 1
  %xtraiter = and i64 %3, 1
  %lcmp.mod.not = icmp eq i64 %xtraiter, 0
  br i1 %lcmp.mod.not, label %edge.append.prol.loopexit, label %edge.append.prol

edge.append.prol:                                 ; preds = %edge.append.preheader
  %.183.prol = getelementptr i64, ptr addrspace(1) %targets, i64 %.162
  %.184.prol = load i64, ptr addrspace(1) %.183.prol, align 8
  %.191.prol = mul i64 %.180.lcssa2332, %walker_count
  %gep.prol = getelementptr i64, ptr addrspace(1) %.58, i64 %.191.prol
  store i64 %.184.prol, ptr addrspace(1) %gep.prol, align 8
  %.195.prol = add i64 %.180.lcssa2332, 1
  %.196.prol = icmp eq i64 %.195.prol, %queue_capacity
  %.197.prol = select i1 %.196.prol, i64 0, i64 %.195.prol
  %.198.prol = add nuw i64 %.162, 1
  br label %edge.append.prol.loopexit

edge.append.prol.loopexit:                        ; preds = %edge.append.prol, %edge.append.preheader
  %.1803.unr = phi i64 [ %.180.lcssa2332, %edge.append.preheader ], [ %.197.prol, %edge.append.prol ]
  %.1792.unr = phi i64 [ %.162, %edge.append.preheader ], [ %.198.prol, %edge.append.prol ]
  %.197.lcssa.unr = phi i64 [ poison, %edge.append.preheader ], [ %.197.prol, %edge.append.prol ]
  %4 = icmp eq i64 %.165, %.neg
  br i1 %4, label %edges.end, label %edge.append

advance:                                          ; preds = %edges.end.1, %round.pop
  %.229.lcssa24 = phi i64 [ %.229.lcssa, %edges.end.1 ], [ %.229.lcssa2531, %round.pop ]
  %.180.lcssa22 = phi i64 [ %.180.lcssa, %edges.end.1 ], [ %.180.lcssa2332, %round.pop ]
  %.15220 = phi i64 [ %.152, %edges.end.1 ], [ %.1522133, %round.pop ]
  %.25117 = phi i64 [ %.251, %edges.end.1 ], [ %.124, %round.pop ]
  %.20215 = phi i64 [ %.202, %edges.end.1 ], [ %.105, %round.pop ]
  %.82 = icmp ne i64 %.20215, 0
  %.85 = icmp ne i64 %.25117, 0
  %.86 = and i1 %.82, %.85
  br i1 %.86, label %round.pop, label %finish

finish:                                           ; preds = %advance, %start
  %.15221.lcssa = phi i64 [ %.28, %start ], [ %.15220, %advance ]
  %.260 = getelementptr i64, ptr addrspace(1) %results, i64 %index
  store i64 %.15221.lcssa, ptr addrspace(1) %.260, align 8
  %.262 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 0, ptr addrspace(1) %.262, align 4
  br label %done

done:                                             ; preds = %finish, %entry
  ret void

edge.append:                                      ; preds = %edge.append.prol.loopexit, %edge.append
  %.1803 = phi i64 [ %.197.1, %edge.append ], [ %.1803.unr, %edge.append.prol.loopexit ]
  %.1792 = phi i64 [ %.198.1, %edge.append ], [ %.1792.unr, %edge.append.prol.loopexit ]
  %.183 = getelementptr i64, ptr addrspace(1) %targets, i64 %.1792
  %.184 = load i64, ptr addrspace(1) %.183, align 8
  %.191 = mul i64 %.1803, %walker_count
  %gep = getelementptr i64, ptr addrspace(1) %.58, i64 %.191
  store i64 %.184, ptr addrspace(1) %gep, align 8
  %.195 = add i64 %.1803, 1
  %.196 = icmp eq i64 %.195, %queue_capacity
  %.197 = select i1 %.196, i64 0, i64 %.195
  %5 = getelementptr i64, ptr addrspace(1) %targets, i64 %.1792
  %.183.1 = getelementptr i8, ptr addrspace(1) %5, i64 8
  %.184.1 = load i64, ptr addrspace(1) %.183.1, align 8
  %.191.1 = mul i64 %.197, %walker_count
  %gep.1 = getelementptr i64, ptr addrspace(1) %.58, i64 %.191.1
  store i64 %.184.1, ptr addrspace(1) %gep.1, align 8
  %.195.1 = add i64 %.197, 1
  %.196.1 = icmp eq i64 %.195.1, %queue_capacity
  %.197.1 = select i1 %.196.1, i64 0, i64 %.195.1
  %.198.1 = add nuw i64 %.1792, 2
  %.181.1 = icmp ult i64 %.198.1, %.165
  br i1 %.181.1, label %edge.append, label %edges.end

edges.end:                                        ; preds = %edge.append.prol.loopexit, %edge.append, %ability
  %.180.lcssa = phi i64 [ %.180.lcssa2332, %ability ], [ %.197.lcssa.unr, %edge.append.prol.loopexit ], [ %.197.1, %edge.append ]
  %.172 = sub i64 %.105, %.162
  %.202 = add i64 %.172, %.165
  %.210 = getelementptr i64, ptr addrspace(1) %2, i64 %.113
  %.211 = load i64, ptr addrspace(1) %.210, align 8
  %.213 = getelementptr i8, ptr addrspace(1) %.210, i64 8
  %.214 = load i64, ptr addrspace(1) %.213, align 8
  %.2306 = icmp ult i64 %.211, %.214
  br i1 %.2306, label %edge.append.1.preheader, label %edges.end.1

edge.append.1.preheader:                          ; preds = %edges.end
  %6 = sub nuw i64 %.214, %.211
  %.neg49 = add i64 %.211, 1
  %xtraiter47 = and i64 %6, 1
  %lcmp.mod48.not = icmp eq i64 %xtraiter47, 0
  br i1 %lcmp.mod48.not, label %edge.append.1.prol.loopexit, label %edge.append.1.prol

edge.append.1.prol:                               ; preds = %edge.append.1.preheader
  %.232.prol = getelementptr i64, ptr addrspace(1) %targets, i64 %.211
  %.233.prol = load i64, ptr addrspace(1) %.232.prol, align 8
  %.239.prol = add i64 %.229.lcssa2531, %queue_capacity
  %.240.prol = mul i64 %.239.prol, %walker_count
  %gep5.prol = getelementptr i64, ptr addrspace(1) %.58, i64 %.240.prol
  store i64 %.233.prol, ptr addrspace(1) %gep5.prol, align 8
  %.244.prol = add i64 %.229.lcssa2531, 1
  %.245.prol = icmp eq i64 %.244.prol, %queue_capacity
  %.246.prol = select i1 %.245.prol, i64 0, i64 %.244.prol
  %.247.prol = add nuw i64 %.211, 1
  br label %edge.append.1.prol.loopexit

edge.append.1.prol.loopexit:                      ; preds = %edge.append.1.prol, %edge.append.1.preheader
  %.2298.unr = phi i64 [ %.229.lcssa2531, %edge.append.1.preheader ], [ %.246.prol, %edge.append.1.prol ]
  %.2287.unr = phi i64 [ %.211, %edge.append.1.preheader ], [ %.247.prol, %edge.append.1.prol ]
  %.246.lcssa.unr = phi i64 [ poison, %edge.append.1.preheader ], [ %.246.prol, %edge.append.1.prol ]
  %7 = icmp eq i64 %.214, %.neg49
  br i1 %7, label %edges.end.1, label %edge.append.1

edge.append.1:                                    ; preds = %edge.append.1.prol.loopexit, %edge.append.1
  %.2298 = phi i64 [ %.246.1, %edge.append.1 ], [ %.2298.unr, %edge.append.1.prol.loopexit ]
  %.2287 = phi i64 [ %.247.1, %edge.append.1 ], [ %.2287.unr, %edge.append.1.prol.loopexit ]
  %.232 = getelementptr i64, ptr addrspace(1) %targets, i64 %.2287
  %.233 = load i64, ptr addrspace(1) %.232, align 8
  %.239 = add i64 %.2298, %queue_capacity
  %.240 = mul i64 %.239, %walker_count
  %gep5 = getelementptr i64, ptr addrspace(1) %.58, i64 %.240
  store i64 %.233, ptr addrspace(1) %gep5, align 8
  %.244 = add i64 %.2298, 1
  %.245 = icmp eq i64 %.244, %queue_capacity
  %.246 = select i1 %.245, i64 0, i64 %.244
  %8 = getelementptr i64, ptr addrspace(1) %targets, i64 %.2287
  %.232.1 = getelementptr i8, ptr addrspace(1) %8, i64 8
  %.233.1 = load i64, ptr addrspace(1) %.232.1, align 8
  %.239.1 = add i64 %.246, %queue_capacity
  %.240.1 = mul i64 %.239.1, %walker_count
  %gep5.1 = getelementptr i64, ptr addrspace(1) %.58, i64 %.240.1
  store i64 %.233.1, ptr addrspace(1) %gep5.1, align 8
  %.244.1 = add i64 %.246, 1
  %.245.1 = icmp eq i64 %.244.1, %queue_capacity
  %.246.1 = select i1 %.245.1, i64 0, i64 %.244.1
  %.247.1 = add nuw i64 %.2287, 2
  %.230.1 = icmp ult i64 %.247.1, %.214
  br i1 %.230.1, label %edge.append.1, label %edges.end.1

edges.end.1:                                      ; preds = %edge.append.1.prol.loopexit, %edge.append.1, %edges.end
  %.229.lcssa = phi i64 [ %.229.lcssa2531, %edges.end ], [ %.246.lcssa.unr, %edge.append.1.prol.loopexit ], [ %.246.1, %edge.append.1 ]
  %.221 = sub i64 %.124, %.211
  %.251 = add i64 %.221, %.214
  br label %advance
}

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 0, 2147483647) i32 @llvm.nvvm.read.ptx.sreg.ctaid.x() #1

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 1, 1025) i32 @llvm.nvvm.read.ptx.sreg.ntid.x() #1

; Function Attrs: mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 0, 1024) i32 @llvm.nvvm.read.ptx.sreg.tid.x() #1

attributes #0 = { nofree norecurse nosync nounwind memory(argmem: readwrite) }
attributes #1 = { mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none) }
