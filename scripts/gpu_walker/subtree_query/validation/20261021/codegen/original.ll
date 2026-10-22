; ModuleID = '<string>'
source_filename = "<string>"
target datalayout = "e-p6:32:32-i64:64-i128:128-i256:256-v16:16-v32:32-n16:32:64"
target triple = "nvptx64-nvidia-cuda"

define ptx_kernel void @jac_SubtreeQuery_csr_batch(ptr addrspace(1) %values, ptr addrspace(1) %values_1, ptr addrspace(1) %offsets, ptr addrspace(1) %targets, ptr addrspace(1) %heads, ptr addrspace(1) %initial_total, ptr addrspace(1) %initial_1, ptr addrspace(1) %initial_2, ptr addrspace(1) %initial_3, ptr addrspace(1) %initial_4, ptr addrspace(1) %results, ptr addrspace(1) %results_1, ptr addrspace(1) %results_2, ptr addrspace(1) %results_3, ptr addrspace(1) %results_4, ptr addrspace(1) %status, ptr addrspace(1) %queue, i64 %node_count, i64 %edge_count, i64 %walker_count, i64 %queue_capacity, i64 %max_visits) {
entry:
  %.24 = call i32 @llvm.nvvm.read.ptx.sreg.ctaid.x()
  %.25 = zext i32 %.24 to i64
  %.26 = call i32 @llvm.nvvm.read.ptx.sreg.ntid.x()
  %.27 = zext i32 %.26 to i64
  %.28 = call i32 @llvm.nvvm.read.ptx.sreg.tid.x()
  %.29 = zext i32 %.28 to i64
  %.30 = mul i64 %.25, %.27
  %index = add i64 %.30, %.29
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
  %.48 = icmp ugt i64 %queue_capacity, 0
  br i1 %.48, label %queue.ready, label %queue.capacity.exceeded

queue.ready:                                      ; preds = %queue.init
  %.50 = getelementptr i64, ptr addrspace(1) %queue, i64 %index
  store i64 %.34, ptr addrspace(1) %.50, align 8
  %.52 = icmp eq i64 %queue_capacity, 1
  %.53 = select i1 %.52, i64 0, i64 1
  br label %queue.check

queue.check:                                      ; preds = %advance, %queue.ready
  %read.pos = phi i64 [ 0, %queue.ready ], [ %.63, %advance ]
  %write.pos = phi i64 [ %.53, %queue.ready ], [ %tail, %advance ]
  %pending = phi i64 [ 1, %queue.ready ], [ %.132, %advance ]
  %steps = phi i64 [ 0, %queue.ready ], [ %.133, %advance ]
  %count = phi i64 [ %.36, %queue.ready ], [ %.95, %advance ]
  %total = phi i64 [ %.38, %queue.ready ], [ %.96, %advance ]
  %has_alert = phi i1 [ %.41, %queue.ready ], [ %.97, %advance ]
  %visited = phi i64 [ %.43, %queue.ready ], [ %.98, %advance ]
  %threshold = phi i64 [ %.45, %queue.ready ], [ %.99, %advance ]
  %.55 = icmp eq i64 %pending, 0
  br i1 %.55, label %finish, label %queue.pop

queue.pop:                                        ; preds = %queue.check
  %.57 = mul i64 %read.pos, %walker_count
  %.58 = add i64 %.57, %index
  %.59 = getelementptr i64, ptr addrspace(1) %queue, i64 %.58
  %.60 = load i64, ptr addrspace(1) %.59, align 8
  %.61 = add i64 %read.pos, 1
  %.62 = icmp eq i64 %.61, %queue_capacity
  %.63 = select i1 %.62, i64 0, i64 %.61
  %.64 = sub i64 %pending, 1
  %.65 = icmp sge i64 %.60, 0
  %.66 = icmp ult i64 %.60, %node_count
  %.67 = and i1 %.65, %.66
  br i1 %.67, label %visit.limit, label %invalid.node

visit.limit:                                      ; preds = %queue.pop
  %.69 = icmp ult i64 %steps, %max_visits
  br i1 %.69, label %ability, label %visit.limit.exceeded

ability:                                          ; preds = %visit.limit
  %.71 = getelementptr i64, ptr addrspace(1) %values, i64 %.60
  %.72 = load i64, ptr addrspace(1) %.71, align 8
  %.73 = getelementptr i64, ptr addrspace(1) %values_1, i64 %.60
  %.74 = load i64, ptr addrspace(1) %.73, align 8
  %.75 = icmp ne i64 %.74, 0
  %.76 = call { i64, i1 } @llvm.sadd.with.overflow.i64(i64 %visited, i64 1)
  %.77 = extractvalue { i64, i1 } %.76, 0
  %.78 = extractvalue { i64, i1 } %.76, 1
  br i1 %.78, label %integer.overflow, label %int.ok

queue.room:                                       ; preds = %update.end
  %.111 = sub i64 %.104, %.101
  %.112 = sub i64 %queue_capacity, %.64
  %.113 = icmp ule i64 %.111, %.112
  br i1 %.113, label %edges.check, label %queue.capacity.exceeded

edges.check:                                      ; preds = %queue.append, %queue.room
  %edge = phi i64 [ %.101, %queue.room ], [ %.130, %queue.append ]
  %tail = phi i64 [ %write.pos, %queue.room ], [ %.129, %queue.append ]
  %.115 = icmp ult i64 %edge, %.104
  br i1 %.115, label %edge.read, label %advance

edge.read:                                        ; preds = %edges.check
  %.117 = getelementptr i64, ptr addrspace(1) %targets, i64 %edge
  %.118 = load i64, ptr addrspace(1) %.117, align 8
  %.119 = icmp sge i64 %.118, 0
  %.120 = icmp ult i64 %.118, %node_count
  %.121 = and i1 %.119, %.120
  br i1 %.121, label %queue.append, label %invalid.node

queue.append:                                     ; preds = %edge.read
  %.123 = mul i64 %tail, %walker_count
  %.124 = add i64 %.123, %index
  %.125 = getelementptr i64, ptr addrspace(1) %queue, i64 %.124
  store i64 %.118, ptr addrspace(1) %.125, align 8
  %.127 = add i64 %tail, 1
  %.128 = icmp eq i64 %.127, %queue_capacity
  %.129 = select i1 %.128, i64 0, i64 %.127
  %.130 = add i64 %edge, 1
  br label %edges.check

advance:                                          ; preds = %edges.check
  %.132 = add i64 %.64, %.111
  %.133 = add i64 %steps, 1
  br label %queue.check

finish:                                           ; preds = %queue.check, %start
  %.135 = phi i64 [ %.36, %start ], [ %count, %queue.check ]
  %.136 = phi i64 [ %.38, %start ], [ %total, %queue.check ]
  %.137 = phi i1 [ %.41, %start ], [ %has_alert, %queue.check ]
  %.138 = phi i64 [ %.43, %start ], [ %visited, %queue.check ]
  %.139 = phi i64 [ %.45, %start ], [ %threshold, %queue.check ]
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
  store i64 %.139, ptr addrspace(1) %.149, align 8
  %.151 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 0, ptr addrspace(1) %.151, align 4
  br label %done

invalid.node:                                     ; preds = %edge.read, %queue.pop
  %.154 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 1, ptr addrspace(1) %.154, align 4
  br label %done

visit.limit.exceeded:                             ; preds = %visit.limit
  %.157 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 2, ptr addrspace(1) %.157, align 4
  br label %done

integer.overflow:                                 ; preds = %int.ok.1, %update.then, %ability
  %.160 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 3, ptr addrspace(1) %.160, align 4
  br label %done

integer.modulo.zero:                              ; No predecessors!
  %.163 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 4, ptr addrspace(1) %.163, align 4
  br label %done

invalid.csr.offsets:                              ; preds = %update.end
  %.166 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 5, ptr addrspace(1) %.166, align 4
  br label %done

queue.capacity.exceeded:                          ; preds = %queue.room, %queue.init
  %.169 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 6, ptr addrspace(1) %.169, align 4
  br label %done

done:                                             ; preds = %report.capacity.exceeded, %queue.capacity.exceeded, %invalid.csr.offsets, %integer.modulo.zero, %integer.overflow, %visit.limit.exceeded, %invalid.node, %finish, %entry
  ret void

report.capacity.exceeded:                         ; No predecessors!
  %.172 = getelementptr i32, ptr addrspace(1) %status, i64 %index
  store i32 7, ptr addrspace(1) %.172, align 4
  br label %done

int.ok:                                           ; preds = %ability
  %.80 = icmp sge i64 %.72, %threshold
  br i1 %.80, label %update.then, label %update.else

update.then:                                      ; preds = %int.ok
  %.82 = call { i64, i1 } @llvm.sadd.with.overflow.i64(i64 %count, i64 1)
  %.83 = extractvalue { i64, i1 } %.82, 0
  %.84 = extractvalue { i64, i1 } %.82, 1
  br i1 %.84, label %integer.overflow, label %int.ok.1

update.else:                                      ; preds = %int.ok
  br label %update.end

update.end:                                       ; preds = %bool.end, %update.else
  %.95 = phi i64 [ %.83, %bool.end ], [ %count, %update.else ]
  %.96 = phi i64 [ %.87, %bool.end ], [ %total, %update.else ]
  %.97 = phi i1 [ %.92, %bool.end ], [ %has_alert, %update.else ]
  %.98 = phi i64 [ %.77, %bool.end ], [ %.77, %update.else ]
  %.99 = phi i64 [ %threshold, %bool.end ], [ %threshold, %update.else ]
  %.100 = getelementptr i64, ptr addrspace(1) %offsets, i64 %.60
  %.101 = load i64, ptr addrspace(1) %.100, align 8
  %.102 = add i64 %.60, 1
  %.103 = getelementptr i64, ptr addrspace(1) %offsets, i64 %.102
  %.104 = load i64, ptr addrspace(1) %.103, align 8
  %.105 = icmp sge i64 %.101, 0
  %.106 = icmp ule i64 %.101, %.104
  %.107 = icmp ule i64 %.104, %edge_count
  %.108 = and i1 %.106, %.107
  %.109 = and i1 %.105, %.108
  br i1 %.109, label %queue.room, label %invalid.csr.offsets

int.ok.1:                                         ; preds = %update.then
  %.86 = call { i64, i1 } @llvm.sadd.with.overflow.i64(i64 %total, i64 %.72)
  %.87 = extractvalue { i64, i1 } %.86, 0
  %.88 = extractvalue { i64, i1 } %.86, 1
  br i1 %.88, label %integer.overflow, label %int.ok.2

int.ok.2:                                         ; preds = %int.ok.1
  br i1 %has_alert, label %bool.end, label %bool.right

bool.right:                                       ; preds = %int.ok.2
  br label %bool.end

bool.end:                                         ; preds = %bool.right, %int.ok.2
  %.92 = phi i1 [ %has_alert, %int.ok.2 ], [ %.75, %bool.right ]
  br label %update.end
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 0, 2147483647) i32 @llvm.nvvm.read.ptx.sreg.ctaid.x() #0

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 1, 1025) i32 @llvm.nvvm.read.ptx.sreg.ntid.x() #0

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare noundef range(i32 0, 1024) i32 @llvm.nvvm.read.ptx.sreg.tid.x() #0

; Function Attrs: nocallback nocreateundeforpoison nofree nosync nounwind speculatable willreturn memory(none)
declare { i64, i1 } @llvm.sadd.with.overflow.i64(i64, i64) #1

attributes #0 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #1 = { nocallback nocreateundeforpoison nofree nosync nounwind speculatable willreturn memory(none) }
