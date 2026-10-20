glob POSIX_FLOOR_SOURCE_SHA256: str = "aa26ba72ec172690712d049e0cfc991481bad7e7318f3343a4e5ed6c38f65e27",
     POSIX_FLOOR_IR_LINUX_X86_64: str = r"""
%struct.stat = type { i64, i64, i64, i32, i32, i32, i32, i64, i64, i64, i64, %struct.timespec, %struct.timespec, %struct.timespec, [3 x i64] }
%struct.timespec = type { i64, i64 }
%struct.passwd = type { ptr, ptr, i32, i32, ptr, ptr, ptr }

@stdin = external local_unnamed_addr global ptr, align 8
@stdout = external local_unnamed_addr global ptr, align 8
@stderr = external local_unnamed_addr global ptr, align 8
@.str = private unnamed_addr constant [15 x i8] c"/proc/self/exe\00", align 1
@switch.table.__jac_addrinfo_layout = private unnamed_addr constant [5 x i64] [i64 16, i64 24, i64 40, i64 48, i64 10], align 8
@switch.table.__jac_clock_id = private unnamed_addr constant [6 x i64] [i64 0, i64 1, i64 2, i64 3, i64 4, i64 1], align 8

define hidden ptr @__jac_errno() local_unnamed_addr #0 {
  %1 = tail call ptr @__errno_location() #14
  ret ptr %1
}

declare ptr @__errno_location() local_unnamed_addr #1

define hidden ptr @__jac_stdio(i32 noundef %0) local_unnamed_addr #2 {
  %2 = icmp eq i32 %0, 1
  %3 = icmp eq i32 %0, 0
  %4 = load ptr, ptr @stdin, align 8
  %5 = load ptr, ptr @stdout, align 8
  %6 = load ptr, ptr @stderr, align 8
  %7 = select i1 %2, ptr %5, ptr %6
  %8 = select i1 %3, ptr %4, ptr %7
  ret ptr %8
}

define hidden noundef i32 @__jac_platform_id() local_unnamed_addr #3 {
  ret i32 0
}

define hidden range(i32 -1, 1) i32 @__jac_stat(ptr noundef %0, ptr noundef writeonly captures(none) %1) local_unnamed_addr #4 {
  %3 = alloca %struct.stat, align 8
  call void @llvm.lifetime.start.p0(i64 144, ptr nonnull %3) #15
  %4 = call i64 (i64, ...) @syscall(i64 noundef 262, i32 noundef -100, ptr noundef %0, ptr noundef nonnull %3, i32 noundef 0) #15
  %5 = icmp eq i64 %4, 0
  br i1 %5, label %6, label %16

6:                                                ; preds = %2
  %7 = getelementptr inbounds nuw i8, ptr %3, i64 88
  %8 = getelementptr inbounds nuw i8, ptr %1, i64 16
  %9 = load <2 x i64>, ptr %7, align 8
  store <2 x i64> %9, ptr %8, align 8
  %10 = getelementptr inbounds nuw i8, ptr %3, i64 24
  %11 = load i32, ptr %10, align 8
  %12 = zext i32 %11 to i64
  store i64 %12, ptr %1, align 8
  %13 = getelementptr inbounds nuw i8, ptr %3, i64 48
  %14 = load i64, ptr %13, align 8
  %15 = getelementptr inbounds nuw i8, ptr %1, i64 8
  store i64 %14, ptr %15, align 8
  br label %16

16:                                               ; preds = %2, %6
  %17 = phi i32 [ 0, %6 ], [ -1, %2 ]
  call void @llvm.lifetime.end.p0(i64 144, ptr nonnull %3) #15
  ret i32 %17
}

declare void @llvm.lifetime.start.p0(i64 immarg, ptr captures(none)) #5

declare i64 @syscall(i64 noundef, ...) local_unnamed_addr #6

declare void @llvm.lifetime.end.p0(i64 immarg, ptr captures(none)) #5

define hidden noalias noundef ptr @__jac_opendir(ptr noundef readonly captures(none) %0) local_unnamed_addr #7 {
  %2 = tail call noalias ptr @opendir(ptr noundef %0)
  ret ptr %2
}

declare noalias noundef ptr @opendir(ptr noundef readonly captures(none)) local_unnamed_addr #8

define hidden ptr @__jac_readdir(ptr noundef %0) local_unnamed_addr #4 {
  %2 = tail call ptr @readdir(ptr noundef %0) #15
  ret ptr %2
}

declare ptr @readdir(ptr noundef) local_unnamed_addr

define hidden noundef i32 @__jac_closedir(ptr noundef captures(none) %0) local_unnamed_addr #7 {
  %2 = tail call i32 @closedir(ptr noundef %0)
  ret i32 %2
}

declare noundef i32 @closedir(ptr noundef captures(none)) local_unnamed_addr #8

define hidden nonnull ptr @__jac_dirent_name(ptr noundef readnone captures(ret: address, provenance) %0) local_unnamed_addr #3 {
  %2 = getelementptr inbounds nuw i8, ptr %0, i64 19
  ret ptr %2
}

define hidden noundef i32 @__jac_at_fdcwd() local_unnamed_addr #3 {
  ret i32 -100
}

define hidden range(i64 -9223372036854775808, 9223372036854775807) i64 @__jac_home_dir(ptr noundef %0, ptr noundef writeonly captures(none) %1, i64 noundef %2) local_unnamed_addr #4 {
  %4 = alloca %struct.passwd, align 8
  %5 = alloca ptr, align 8
  %6 = alloca [4096 x i8], align 16
  call void @llvm.lifetime.start.p0(i64 48, ptr nonnull %4) #15
  call void @llvm.lifetime.start.p0(i64 8, ptr nonnull %5) #15
  store ptr null, ptr %5, align 8
  call void @llvm.lifetime.start.p0(i64 4096, ptr nonnull %6) #15
  %7 = load i8, ptr %0, align 1
  %8 = icmp eq i8 %7, 0
  br i1 %8, label %11, label %9

9:                                                ; preds = %3
  %10 = call i32 @getpwnam_r(ptr noundef nonnull %0, ptr noundef nonnull %4, ptr noundef nonnull %6, i64 noundef 4096, ptr noundef nonnull %5) #15
  br label %14

11:                                               ; preds = %3
  %12 = tail call i32 @getuid() #15
  %13 = call i32 @getpwuid_r(i32 noundef %12, ptr noundef nonnull %4, ptr noundef nonnull %6, i64 noundef 4096, ptr noundef nonnull %5) #15
  br label %14

14:                                               ; preds = %11, %9
  %15 = phi i32 [ %10, %9 ], [ %13, %11 ]
  %16 = icmp ne i32 %15, 0
  %17 = load ptr, ptr %5, align 8
  %18 = icmp eq ptr %17, null
  %19 = select i1 %16, i1 true, i1 %18
  br i1 %19, label %29, label %20

20:                                               ; preds = %14
  %21 = getelementptr inbounds nuw i8, ptr %4, i64 32
  %22 = load ptr, ptr %21, align 8
  %23 = icmp eq ptr %22, null
  br i1 %23, label %29, label %24

24:                                               ; preds = %20
  %25 = call i64 @strlen(ptr noundef nonnull dereferenceable(1) %22) #16
  %26 = icmp slt i64 %25, %2
  br i1 %26, label %27, label %29

27:                                               ; preds = %24
  %28 = add nsw i64 %25, 1
  call void @llvm.memcpy.p0.p0.i64(ptr align 1 %1, ptr nonnull align 1 %22, i64 %28, i1 false)
  br label %29

29:                                               ; preds = %27, %24, %20, %14
  %30 = phi i64 [ -1, %14 ], [ -2, %20 ], [ %25, %27 ], [ -1, %24 ]
  call void @llvm.lifetime.end.p0(i64 4096, ptr nonnull %6) #15
  call void @llvm.lifetime.end.p0(i64 8, ptr nonnull %5) #15
  call void @llvm.lifetime.end.p0(i64 48, ptr nonnull %4) #15
  ret i64 %30
}

declare i32 @getpwnam_r(ptr noundef, ptr noundef, ptr noundef, i64 noundef, ptr noundef) local_unnamed_addr

declare i32 @getpwuid_r(i32 noundef, ptr noundef, ptr noundef, i64 noundef, ptr noundef) local_unnamed_addr

declare i32 @getuid() local_unnamed_addr #6

declare i64 @strlen(ptr noundef captures(none)) local_unnamed_addr #10

declare void @llvm.memcpy.p0.p0.i64(ptr noalias writeonly captures(none), ptr noalias readonly captures(none), i64, i1 immarg) #11

define hidden range(i64 -1, -9223372036854775808) i64 @__jac_executable_path(ptr noundef captures(none) %0, i64 noundef %1) local_unnamed_addr #7 {
  %3 = add nsw i64 %1, -1
  %4 = tail call i64 @readlink(ptr noundef nonnull @.str, ptr noundef %0, i64 noundef %3) #15
  %5 = icmp slt i64 %4, 1
  br i1 %5, label %8, label %6

6:                                                ; preds = %2
  %7 = getelementptr inbounds nuw i8, ptr %0, i64 %4
  store i8 0, ptr %7, align 1
  br label %8

8:                                                ; preds = %2, %6
  %9 = phi i64 [ %4, %6 ], [ -1, %2 ]
  ret i64 %9
}

declare noundef i64 @readlink(ptr noundef readonly captures(none), ptr noundef captures(none), i64 noundef) local_unnamed_addr #8

define hidden range(i64 -1, 49) i64 @__jac_addrinfo_layout(i32 noundef %0) local_unnamed_addr #3 {
  %2 = icmp ult i32 %0, 5
  br i1 %2, label %3, label %7

3:                                                ; preds = %1
  %4 = zext nneg i32 %0 to i64
  %5 = getelementptr inbounds nuw [5 x i64], ptr @switch.table.__jac_addrinfo_layout, i64 0, i64 %4
  %6 = load i64, ptr %5, align 8
  br label %7

7:                                                ; preds = %1, %3
  %8 = phi i64 [ %6, %3 ], [ -1, %1 ]
  ret i64 %8
}

define hidden range(i32 0, 65536) i32 @__jac_sockaddr_family(ptr noundef readonly captures(none) %0) local_unnamed_addr #12 {
  %2 = load i16, ptr %0, align 2
  %3 = zext i16 %2 to i32
  ret i32 %3
}

define hidden range(i64 -1, 5) i64 @__jac_clock_id(i32 noundef %0) local_unnamed_addr #3 {
  %2 = icmp ult i32 %0, 6
  br i1 %2, label %3, label %7

3:                                                ; preds = %1
  %4 = zext nneg i32 %0 to i64
  %5 = getelementptr inbounds nuw [6 x i64], ptr @switch.table.__jac_clock_id, i64 0, i64 %4
  %6 = load i64, ptr %5, align 8
  br label %7

7:                                                ; preds = %1, %3
  %8 = phi i64 [ %6, %3 ], [ -1, %1 ]
  ret i64 %8
}

define hidden i32 @__jac_sleep_ns(i64 noundef %0) local_unnamed_addr #4 {
  %2 = alloca %struct.timespec, align 8
  call void @llvm.lifetime.start.p0(i64 16, ptr nonnull %2) #15
  %3 = call i32 @clock_gettime(i32 noundef 1, ptr noundef nonnull %2) #15
  %4 = icmp eq i32 %3, 0
  br i1 %4, label %8, label %5

5:                                                ; preds = %1
  %6 = tail call ptr @__errno_location() #14
  %7 = load i32, ptr %6, align 4
  br label %24

8:                                                ; preds = %1
  %9 = sdiv i64 %0, 1000000000
  %10 = load i64, ptr %2, align 8
  %11 = add nsw i64 %10, %9
  store i64 %11, ptr %2, align 8
  %12 = srem i64 %0, 1000000000
  %13 = getelementptr inbounds nuw i8, ptr %2, i64 8
  %14 = load i64, ptr %13, align 8
  %15 = add nsw i64 %14, %12
  store i64 %15, ptr %13, align 8
  %16 = icmp sgt i64 %15, 999999999
  br i1 %16, label %17, label %20

17:                                               ; preds = %8
  %18 = add nsw i64 %15, -1000000000
  store i64 %18, ptr %13, align 8
  %19 = add nsw i64 %11, 1
  store i64 %19, ptr %2, align 8
  br label %20

20:                                               ; preds = %17, %8
  br label %21

21:                                               ; preds = %20, %21
  %22 = call i32 @clock_nanosleep(i32 noundef 1, i32 noundef 1, ptr noundef nonnull %2, ptr noundef null) #15
  %23 = icmp eq i32 %22, 4
  br i1 %23, label %21, label %24

24:                                               ; preds = %21, %5
  %25 = phi i32 [ %7, %5 ], [ %22, %21 ]
  call void @llvm.lifetime.end.p0(i64 16, ptr nonnull %2) #15
  ret i32 %25
}

declare i32 @clock_gettime(i32 noundef, ptr noundef) local_unnamed_addr #6

declare i32 @clock_nanosleep(i32 noundef, i32 noundef, ptr noundef, ptr noundef) local_unnamed_addr

define hidden i64 @__jac_malloc_size(ptr noundef %0) local_unnamed_addr #4 {
  %2 = tail call i64 @malloc_usable_size(ptr noundef %0) #15
  ret i64 %2
}

declare i64 @malloc_usable_size(ptr noundef) local_unnamed_addr #6

define hidden noundef double @__jac_fmadd(double noundef %0, double noundef %1, double noundef %2) local_unnamed_addr #3 {
  %4 = fmul double %0, %1
  %5 = fadd double %4, %2
  ret double %5
}

define hidden noundef ptr @__jac_va_list(ptr noundef readnone returned captures(ret: address, provenance) %0) local_unnamed_addr #3 {
  ret ptr %0
}

define hidden i64 @__jac_va_i64(ptr noundef readonly captures(none) %0) local_unnamed_addr #13 {
  %2 = load ptr, ptr %0, align 8
  %3 = load i32, ptr %2, align 8
  %4 = icmp ult i32 %3, 41
  br i1 %4, label %5, label %11

5:                                                ; preds = %1
  %6 = getelementptr inbounds nuw i8, ptr %2, i64 16
  %7 = load ptr, ptr %6, align 8
  %8 = zext nneg i32 %3 to i64
  %9 = getelementptr i8, ptr %7, i64 %8
  %10 = add nuw nsw i32 %3, 8
  store i32 %10, ptr %2, align 8
  br label %15

11:                                               ; preds = %1
  %12 = getelementptr inbounds nuw i8, ptr %2, i64 8
  %13 = load ptr, ptr %12, align 8
  %14 = getelementptr i8, ptr %13, i64 8
  store ptr %14, ptr %12, align 8
  br label %15

15:                                               ; preds = %11, %5
  %16 = phi ptr [ %9, %5 ], [ %13, %11 ]
  %17 = load i64, ptr %16, align 8
  ret i64 %17
}

define hidden double @__jac_va_f64(ptr noundef readonly captures(none) %0) local_unnamed_addr #13 {
  %2 = load ptr, ptr %0, align 8
  %3 = getelementptr inbounds nuw i8, ptr %2, i64 4
  %4 = load i32, ptr %3, align 4
  %5 = icmp ult i32 %4, 161
  br i1 %5, label %6, label %12

6:                                                ; preds = %1
  %7 = getelementptr inbounds nuw i8, ptr %2, i64 16
  %8 = load ptr, ptr %7, align 8
  %9 = zext nneg i32 %4 to i64
  %10 = getelementptr i8, ptr %8, i64 %9
  %11 = add nuw nsw i32 %4, 16
  store i32 %11, ptr %3, align 4
  br label %16

12:                                               ; preds = %1
  %13 = getelementptr inbounds nuw i8, ptr %2, i64 8
  %14 = load ptr, ptr %13, align 8
  %15 = getelementptr i8, ptr %14, i64 8
  store ptr %15, ptr %13, align 8
  br label %16

16:                                               ; preds = %12, %6
  %17 = phi ptr [ %10, %6 ], [ %14, %12 ]
  %18 = load double, ptr %17, align 8
  ret double %18
}

attributes #0 = { mustprogress nofree nosync nounwind willreturn memory(none) uwtable(sync) }
attributes #1 = { mustprogress nofree nosync nounwind willreturn memory(none) }
attributes #2 = { mustprogress nofree norecurse nosync nounwind willreturn memory(read, argmem: none, inaccessiblemem: none) uwtable(sync) }
attributes #3 = { mustprogress nofree norecurse nosync nounwind willreturn memory(none) uwtable(sync) }
attributes #4 = { nounwind uwtable(sync) }
attributes #5 = { mustprogress nocallback nofree nosync nounwind willreturn memory(argmem: readwrite) }
attributes #6 = { nounwind }
attributes #7 = { nofree nounwind uwtable(sync) }
attributes #8 = { nofree nounwind }
attributes #10 = { mustprogress nocallback nofree nounwind willreturn memory(argmem: read) }
attributes #11 = { mustprogress nocallback nofree nounwind willreturn memory(argmem: readwrite) }
attributes #12 = { mustprogress nofree norecurse nosync nounwind willreturn memory(argmem: read) uwtable(sync) }
attributes #13 = { mustprogress nofree norecurse nosync nounwind willreturn memory(readwrite, inaccessiblemem: none) uwtable(sync) }
attributes #14 = { nounwind willreturn memory(none) }
attributes #15 = { nounwind }
attributes #16 = { nounwind willreturn memory(read) }
""",
     POSIX_FLOOR_IR_LINUX_AARCH64: str = r"""
%struct.stat = type { i64, i64, i32, i32, i32, i32, i64, i64, i64, i32, i32, i64, %struct.timespec, %struct.timespec, %struct.timespec, [2 x i32] }
%struct.timespec = type { i64, i64 }
%struct.passwd = type { ptr, ptr, i32, i32, ptr, ptr, ptr }

@stdin = external local_unnamed_addr global ptr, align 8
@stdout = external local_unnamed_addr global ptr, align 8
@stderr = external local_unnamed_addr global ptr, align 8
@.str = private unnamed_addr constant [15 x i8] c"/proc/self/exe\00", align 1
@switch.table.__jac_addrinfo_layout = private unnamed_addr constant [5 x i64] [i64 16, i64 24, i64 40, i64 48, i64 10], align 8
@switch.table.__jac_clock_id = private unnamed_addr constant [6 x i64] [i64 0, i64 1, i64 2, i64 3, i64 4, i64 1], align 8

define hidden ptr @__jac_errno() local_unnamed_addr #0 {
  %1 = tail call ptr @__errno_location() #15
  ret ptr %1
}

declare ptr @__errno_location() local_unnamed_addr #1

define hidden ptr @__jac_stdio(i32 noundef %0) local_unnamed_addr #2 {
  %2 = icmp eq i32 %0, 1
  %3 = icmp eq i32 %0, 0
  %4 = load ptr, ptr @stdin, align 8
  %5 = load ptr, ptr @stdout, align 8
  %6 = load ptr, ptr @stderr, align 8
  %7 = select i1 %2, ptr %5, ptr %6
  %8 = select i1 %3, ptr %4, ptr %7
  ret ptr %8
}

define hidden noundef i32 @__jac_platform_id() local_unnamed_addr #3 {
  ret i32 0
}

define hidden range(i32 -1, 1) i32 @__jac_stat(ptr noundef %0, ptr noundef writeonly captures(none) %1) local_unnamed_addr #4 {
  %3 = alloca %struct.stat, align 8
  call void @llvm.lifetime.start.p0(i64 128, ptr nonnull %3) #16
  %4 = call i64 (i64, ...) @syscall(i64 noundef 79, i32 noundef -100, ptr noundef %0, ptr noundef nonnull %3, i32 noundef 0) #16
  %5 = icmp eq i64 %4, 0
  br i1 %5, label %6, label %16

6:                                                ; preds = %2
  %7 = getelementptr inbounds nuw i8, ptr %3, i64 88
  %8 = getelementptr inbounds nuw i8, ptr %1, i64 16
  %9 = load <2 x i64>, ptr %7, align 8
  store <2 x i64> %9, ptr %8, align 8
  %10 = getelementptr inbounds nuw i8, ptr %3, i64 16
  %11 = load i32, ptr %10, align 8
  %12 = zext i32 %11 to i64
  store i64 %12, ptr %1, align 8
  %13 = getelementptr inbounds nuw i8, ptr %3, i64 48
  %14 = load i64, ptr %13, align 8
  %15 = getelementptr inbounds nuw i8, ptr %1, i64 8
  store i64 %14, ptr %15, align 8
  br label %16

16:                                               ; preds = %2, %6
  %17 = phi i32 [ 0, %6 ], [ -1, %2 ]
  call void @llvm.lifetime.end.p0(i64 128, ptr nonnull %3) #16
  ret i32 %17
}

declare void @llvm.lifetime.start.p0(i64 immarg, ptr captures(none)) #5

declare i64 @syscall(i64 noundef, ...) local_unnamed_addr #6

declare void @llvm.lifetime.end.p0(i64 immarg, ptr captures(none)) #5

define hidden noalias noundef ptr @__jac_opendir(ptr noundef readonly captures(none) %0) local_unnamed_addr #7 {
  %2 = tail call noalias ptr @opendir(ptr noundef %0)
  ret ptr %2
}

declare noalias noundef ptr @opendir(ptr noundef readonly captures(none)) local_unnamed_addr #8

define hidden ptr @__jac_readdir(ptr noundef %0) local_unnamed_addr #4 {
  %2 = tail call ptr @readdir(ptr noundef %0) #16
  ret ptr %2
}

declare ptr @readdir(ptr noundef) local_unnamed_addr

define hidden noundef i32 @__jac_closedir(ptr noundef captures(none) %0) local_unnamed_addr #7 {
  %2 = tail call i32 @closedir(ptr noundef %0)
  ret i32 %2
}

declare noundef i32 @closedir(ptr noundef captures(none)) local_unnamed_addr #8

define hidden nonnull ptr @__jac_dirent_name(ptr noundef readnone captures(ret: address, provenance) %0) local_unnamed_addr #3 {
  %2 = getelementptr inbounds nuw i8, ptr %0, i64 19
  ret ptr %2
}

define hidden noundef i32 @__jac_at_fdcwd() local_unnamed_addr #3 {
  ret i32 -100
}

define hidden range(i64 -9223372036854775808, 9223372036854775807) i64 @__jac_home_dir(ptr noundef %0, ptr noundef writeonly captures(none) %1, i64 noundef %2) local_unnamed_addr #4 {
  %4 = alloca %struct.passwd, align 8
  %5 = alloca ptr, align 8
  %6 = alloca [4096 x i8], align 1
  call void @llvm.lifetime.start.p0(i64 48, ptr nonnull %4) #16
  call void @llvm.lifetime.start.p0(i64 8, ptr nonnull %5) #16
  store ptr null, ptr %5, align 8
  call void @llvm.lifetime.start.p0(i64 4096, ptr nonnull %6) #16
  %7 = load i8, ptr %0, align 1
  %8 = icmp eq i8 %7, 0
  br i1 %8, label %11, label %9

9:                                                ; preds = %3
  %10 = call i32 @getpwnam_r(ptr noundef nonnull %0, ptr noundef nonnull %4, ptr noundef nonnull %6, i64 noundef 4096, ptr noundef nonnull %5) #16
  br label %14

11:                                               ; preds = %3
  %12 = tail call i32 @getuid() #16
  %13 = call i32 @getpwuid_r(i32 noundef %12, ptr noundef nonnull %4, ptr noundef nonnull %6, i64 noundef 4096, ptr noundef nonnull %5) #16
  br label %14

14:                                               ; preds = %11, %9
  %15 = phi i32 [ %10, %9 ], [ %13, %11 ]
  %16 = icmp ne i32 %15, 0
  %17 = load ptr, ptr %5, align 8
  %18 = icmp eq ptr %17, null
  %19 = select i1 %16, i1 true, i1 %18
  br i1 %19, label %29, label %20

20:                                               ; preds = %14
  %21 = getelementptr inbounds nuw i8, ptr %4, i64 32
  %22 = load ptr, ptr %21, align 8
  %23 = icmp eq ptr %22, null
  br i1 %23, label %29, label %24

24:                                               ; preds = %20
  %25 = call i64 @strlen(ptr noundef nonnull dereferenceable(1) %22) #17
  %26 = icmp slt i64 %25, %2
  br i1 %26, label %27, label %29

27:                                               ; preds = %24
  %28 = add nsw i64 %25, 1
  call void @llvm.memcpy.p0.p0.i64(ptr align 1 %1, ptr nonnull align 1 %22, i64 %28, i1 false)
  br label %29

29:                                               ; preds = %27, %24, %20, %14
  %30 = phi i64 [ -1, %14 ], [ -2, %20 ], [ %25, %27 ], [ -1, %24 ]
  call void @llvm.lifetime.end.p0(i64 4096, ptr nonnull %6) #16
  call void @llvm.lifetime.end.p0(i64 8, ptr nonnull %5) #16
  call void @llvm.lifetime.end.p0(i64 48, ptr nonnull %4) #16
  ret i64 %30
}

declare i32 @getpwnam_r(ptr noundef, ptr noundef, ptr noundef, i64 noundef, ptr noundef) local_unnamed_addr

declare i32 @getpwuid_r(i32 noundef, ptr noundef, ptr noundef, i64 noundef, ptr noundef) local_unnamed_addr

declare i32 @getuid() local_unnamed_addr #6

declare i64 @strlen(ptr noundef captures(none)) local_unnamed_addr #10

declare void @llvm.memcpy.p0.p0.i64(ptr noalias writeonly captures(none), ptr noalias readonly captures(none), i64, i1 immarg) #11

define hidden range(i64 -1, -9223372036854775808) i64 @__jac_executable_path(ptr noundef captures(none) %0, i64 noundef %1) local_unnamed_addr #7 {
  %3 = add nsw i64 %1, -1
  %4 = tail call i64 @readlink(ptr noundef nonnull @.str, ptr noundef %0, i64 noundef %3) #16
  %5 = icmp slt i64 %4, 1
  br i1 %5, label %8, label %6

6:                                                ; preds = %2
  %7 = getelementptr inbounds nuw i8, ptr %0, i64 %4
  store i8 0, ptr %7, align 1
  br label %8

8:                                                ; preds = %2, %6
  %9 = phi i64 [ %4, %6 ], [ -1, %2 ]
  ret i64 %9
}

declare noundef i64 @readlink(ptr noundef readonly captures(none), ptr noundef captures(none), i64 noundef) local_unnamed_addr #8

define hidden range(i64 -1, 49) i64 @__jac_addrinfo_layout(i32 noundef %0) local_unnamed_addr #3 {
  %2 = icmp ult i32 %0, 5
  br i1 %2, label %3, label %7

3:                                                ; preds = %1
  %4 = zext nneg i32 %0 to i64
  %5 = getelementptr inbounds nuw [5 x i64], ptr @switch.table.__jac_addrinfo_layout, i64 0, i64 %4
  %6 = load i64, ptr %5, align 8
  br label %7

7:                                                ; preds = %1, %3
  %8 = phi i64 [ %6, %3 ], [ -1, %1 ]
  ret i64 %8
}

define hidden range(i32 0, 65536) i32 @__jac_sockaddr_family(ptr noundef readonly captures(none) %0) local_unnamed_addr #12 {
  %2 = load i16, ptr %0, align 2
  %3 = zext i16 %2 to i32
  ret i32 %3
}

define hidden range(i64 -1, 5) i64 @__jac_clock_id(i32 noundef %0) local_unnamed_addr #3 {
  %2 = icmp ult i32 %0, 6
  br i1 %2, label %3, label %7

3:                                                ; preds = %1
  %4 = zext nneg i32 %0 to i64
  %5 = getelementptr inbounds nuw [6 x i64], ptr @switch.table.__jac_clock_id, i64 0, i64 %4
  %6 = load i64, ptr %5, align 8
  br label %7

7:                                                ; preds = %1, %3
  %8 = phi i64 [ %6, %3 ], [ -1, %1 ]
  ret i64 %8
}

define hidden i32 @__jac_sleep_ns(i64 noundef %0) local_unnamed_addr #4 {
  %2 = alloca %struct.timespec, align 8
  call void @llvm.lifetime.start.p0(i64 16, ptr nonnull %2) #16
  %3 = call i32 @clock_gettime(i32 noundef 1, ptr noundef nonnull %2) #16
  %4 = icmp eq i32 %3, 0
  br i1 %4, label %8, label %5

5:                                                ; preds = %1
  %6 = tail call ptr @__errno_location() #15
  %7 = load i32, ptr %6, align 4
  br label %25

8:                                                ; preds = %1
  %9 = sdiv i64 %0, 1000000000
  %10 = load i64, ptr %2, align 8
  %11 = add nsw i64 %10, %9
  store i64 %11, ptr %2, align 8
  %12 = mul i64 %9, 1000000000
  %13 = sub i64 %0, %12
  %14 = getelementptr inbounds nuw i8, ptr %2, i64 8
  %15 = load i64, ptr %14, align 8
  %16 = add nsw i64 %15, %13
  store i64 %16, ptr %14, align 8
  %17 = icmp sgt i64 %16, 999999999
  br i1 %17, label %18, label %21

18:                                               ; preds = %8
  %19 = add nsw i64 %16, -1000000000
  store i64 %19, ptr %14, align 8
  %20 = add nsw i64 %11, 1
  store i64 %20, ptr %2, align 8
  br label %21

21:                                               ; preds = %18, %8
  br label %22

22:                                               ; preds = %21, %22
  %23 = call i32 @clock_nanosleep(i32 noundef 1, i32 noundef 1, ptr noundef nonnull %2, ptr noundef null) #16
  %24 = icmp eq i32 %23, 4
  br i1 %24, label %22, label %25

25:                                               ; preds = %22, %5
  %26 = phi i32 [ %7, %5 ], [ %23, %22 ]
  call void @llvm.lifetime.end.p0(i64 16, ptr nonnull %2) #16
  ret i32 %26
}

declare i32 @clock_gettime(i32 noundef, ptr noundef) local_unnamed_addr #6

declare i32 @clock_nanosleep(i32 noundef, i32 noundef, ptr noundef, ptr noundef) local_unnamed_addr

define hidden i64 @__jac_malloc_size(ptr noundef %0) local_unnamed_addr #4 {
  %2 = tail call i64 @malloc_usable_size(ptr noundef %0) #16
  ret i64 %2
}

declare i64 @malloc_usable_size(ptr noundef) local_unnamed_addr #6

define hidden noundef double @__jac_fmadd(double noundef %0, double noundef %1, double noundef %2) local_unnamed_addr #3 {
  %4 = tail call double @llvm.fma.f64(double %0, double %1, double %2)
  ret double %4
}

declare double @llvm.fma.f64(double, double, double) #13

define hidden noundef ptr @__jac_va_list(ptr noundef readnone returned captures(ret: address, provenance) %0) local_unnamed_addr #3 {
  ret ptr %0
}

define hidden i64 @__jac_va_i64(ptr noundef readonly captures(none) %0) local_unnamed_addr #14 {
  %2 = load ptr, ptr %0, align 8
  %3 = getelementptr inbounds nuw i8, ptr %2, i64 24
  %4 = load i32, ptr %3, align 8
  %5 = icmp sgt i32 %4, -1
  br i1 %5, label %14, label %6

6:                                                ; preds = %1
  %7 = add nsw i32 %4, 8
  store i32 %7, ptr %3, align 8
  %8 = icmp samesign ult i32 %4, -7
  br i1 %8, label %9, label %14

9:                                                ; preds = %6
  %10 = getelementptr inbounds nuw i8, ptr %2, i64 8
  %11 = load ptr, ptr %10, align 8
  %12 = sext i32 %4 to i64
  %13 = getelementptr inbounds i8, ptr %11, i64 %12
  br label %17

14:                                               ; preds = %6, %1
  %15 = load ptr, ptr %2, align 8
  %16 = getelementptr inbounds nuw i8, ptr %15, i64 8
  store ptr %16, ptr %2, align 8
  br label %17

17:                                               ; preds = %14, %9
  %18 = phi ptr [ %13, %9 ], [ %15, %14 ]
  %19 = load i64, ptr %18, align 8
  ret i64 %19
}

define hidden double @__jac_va_f64(ptr noundef readonly captures(none) %0) local_unnamed_addr #14 {
  %2 = load ptr, ptr %0, align 8
  %3 = getelementptr inbounds nuw i8, ptr %2, i64 28
  %4 = load i32, ptr %3, align 4
  %5 = icmp sgt i32 %4, -1
  br i1 %5, label %14, label %6

6:                                                ; preds = %1
  %7 = add nsw i32 %4, 16
  store i32 %7, ptr %3, align 4
  %8 = icmp samesign ult i32 %4, -15
  br i1 %8, label %9, label %14

9:                                                ; preds = %6
  %10 = getelementptr inbounds nuw i8, ptr %2, i64 16
  %11 = load ptr, ptr %10, align 8
  %12 = sext i32 %4 to i64
  %13 = getelementptr inbounds i8, ptr %11, i64 %12
  br label %17

14:                                               ; preds = %6, %1
  %15 = load ptr, ptr %2, align 8
  %16 = getelementptr inbounds nuw i8, ptr %15, i64 8
  store ptr %16, ptr %2, align 8
  br label %17

17:                                               ; preds = %14, %9
  %18 = phi ptr [ %13, %9 ], [ %15, %14 ]
  %19 = load double, ptr %18, align 8
  ret double %19
}

attributes #0 = { mustprogress nofree nosync nounwind willreturn memory(none) uwtable(sync) }
attributes #1 = { mustprogress nofree nosync nounwind willreturn memory(none) }
attributes #2 = { mustprogress nofree norecurse nosync nounwind willreturn memory(read, argmem: none, inaccessiblemem: none) uwtable(sync) }
attributes #3 = { mustprogress nofree norecurse nosync nounwind willreturn memory(none) uwtable(sync) }
attributes #4 = { nounwind uwtable(sync) }
attributes #5 = { mustprogress nocallback nofree nosync nounwind willreturn memory(argmem: readwrite) }
attributes #6 = { nounwind }
attributes #7 = { nofree nounwind uwtable(sync) }
attributes #8 = { nofree nounwind }
attributes #10 = { mustprogress nocallback nofree nounwind willreturn memory(argmem: read) }
attributes #11 = { mustprogress nocallback nofree nounwind willreturn memory(argmem: readwrite) }
attributes #12 = { mustprogress nofree norecurse nosync nounwind willreturn memory(argmem: read) uwtable(sync) }
attributes #13 = { mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #14 = { mustprogress nofree norecurse nosync nounwind willreturn memory(readwrite, inaccessiblemem: none) uwtable(sync) }
attributes #15 = { nounwind willreturn memory(none) }
attributes #16 = { nounwind }
attributes #17 = { nounwind willreturn memory(read) }
""",
     POSIX_FLOOR_IR_MACOS_AARCH64: str = r"""
%struct.stat = type { i32, i16, i16, i64, i32, i32, i32, %struct.timespec, %struct.timespec, %struct.timespec, %struct.timespec, i64, i64, i32, i32, i32, i32, [2 x i64] }
%struct.timespec = type { i64, i64 }
%struct.passwd = type { ptr, ptr, i32, i32, i64, ptr, ptr, ptr, ptr, i64 }

@__stdinp = external local_unnamed_addr global ptr, align 8
@__stdoutp = external local_unnamed_addr global ptr, align 8
@__stderrp = external local_unnamed_addr global ptr, align 8
@switch.table.__jac_addrinfo_layout = private unnamed_addr constant [5 x i64] [i64 16, i64 32, i64 40, i64 48, i64 30], align 8
@switch.table.__jac_clock_id = private unnamed_addr constant [6 x i64] [i64 0, i64 6, i64 12, i64 16, i64 4, i64 8], align 8

define hidden ptr @__jac_errno() local_unnamed_addr #0 {
  %1 = tail call ptr @__error() #10
  ret ptr %1
}

declare ptr @__error() local_unnamed_addr

define hidden ptr @__jac_stdio(i32 noundef %0) local_unnamed_addr #2 {
  %2 = icmp eq i32 %0, 1
  %3 = icmp eq i32 %0, 0
  %4 = load ptr, ptr @__stdinp, align 8
  %5 = load ptr, ptr @__stdoutp, align 8
  %6 = load ptr, ptr @__stderrp, align 8
  %7 = select i1 %2, ptr %5, ptr %6
  %8 = select i1 %3, ptr %4, ptr %7
  ret ptr %8
}

define hidden noundef i32 @__jac_platform_id() local_unnamed_addr #3 {
  ret i32 1
}

define hidden range(i32 -1, 1) i32 @__jac_stat(ptr noundef %0, ptr noundef writeonly captures(none) %1) local_unnamed_addr #0 {
  %3 = alloca %struct.stat, align 8
  call void @llvm.lifetime.start.p0(i64 144, ptr nonnull %3) #10
  %4 = call i32 @"\01_stat"(ptr noundef %0, ptr noundef nonnull %3) #10
  %5 = icmp eq i32 %4, 0
  br i1 %5, label %6, label %16

6:                                                ; preds = %2
  %7 = getelementptr inbounds nuw i8, ptr %3, i64 48
  %8 = getelementptr inbounds nuw i8, ptr %1, i64 16
  %9 = load <2 x i64>, ptr %7, align 8
  store <2 x i64> %9, ptr %8, align 8
  %10 = getelementptr inbounds nuw i8, ptr %3, i64 4
  %11 = load i16, ptr %10, align 4
  %12 = zext i16 %11 to i64
  store i64 %12, ptr %1, align 8
  %13 = getelementptr inbounds nuw i8, ptr %3, i64 96
  %14 = load i64, ptr %13, align 8
  %15 = getelementptr inbounds nuw i8, ptr %1, i64 8
  store i64 %14, ptr %15, align 8
  br label %16

16:                                               ; preds = %2, %6
  %17 = phi i32 [ 0, %6 ], [ -1, %2 ]
  call void @llvm.lifetime.end.p0(i64 144, ptr nonnull %3) #10
  ret i32 %17
}

declare void @llvm.lifetime.start.p0(i64 immarg, ptr captures(none)) #4

declare i32 @"\01_stat"(ptr noundef, ptr noundef) local_unnamed_addr

declare void @llvm.lifetime.end.p0(i64 immarg, ptr captures(none)) #4

define hidden ptr @__jac_opendir(ptr noundef %0) local_unnamed_addr #0 {
  %2 = tail call ptr @"\01_opendir"(ptr noundef %0) #10
  ret ptr %2
}

declare ptr @"\01_opendir"(ptr noundef) local_unnamed_addr

define hidden ptr @__jac_readdir(ptr noundef %0) local_unnamed_addr #0 {
  %2 = tail call ptr @"\01_readdir"(ptr noundef %0) #10
  ret ptr %2
}

declare ptr @"\01_readdir"(ptr noundef) local_unnamed_addr

define hidden i32 @__jac_closedir(ptr noundef %0) local_unnamed_addr #0 {
  %2 = tail call i32 @"\01_closedir"(ptr noundef %0) #10
  ret i32 %2
}

declare i32 @"\01_closedir"(ptr noundef) local_unnamed_addr

define hidden nonnull ptr @__jac_dirent_name(ptr noundef readnone captures(ret: address, provenance) %0) local_unnamed_addr #3 {
  %2 = getelementptr inbounds nuw i8, ptr %0, i64 21
  ret ptr %2
}

define hidden noundef i32 @__jac_at_fdcwd() local_unnamed_addr #3 {
  ret i32 -2
}

define hidden range(i64 -9223372036854775808, 9223372036854775807) i64 @__jac_home_dir(ptr noundef %0, ptr noundef %1, i64 noundef %2) local_unnamed_addr #0 {
  %4 = alloca %struct.passwd, align 8
  %5 = alloca ptr, align 8
  %6 = alloca [4096 x i8], align 1
  call void @llvm.lifetime.start.p0(i64 72, ptr nonnull %4) #10
  call void @llvm.lifetime.start.p0(i64 8, ptr nonnull %5) #10
  store ptr null, ptr %5, align 8
  call void @llvm.lifetime.start.p0(i64 4096, ptr nonnull %6) #10
  %7 = load i8, ptr %0, align 1
  %8 = icmp eq i8 %7, 0
  br i1 %8, label %11, label %9

9:                                                ; preds = %3
  %10 = call i32 @getpwnam_r(ptr noundef nonnull %0, ptr noundef nonnull %4, ptr noundef nonnull %6, i64 noundef 4096, ptr noundef nonnull %5) #10
  br label %14

11:                                               ; preds = %3
  %12 = tail call i32 @getuid() #10
  %13 = call i32 @getpwuid_r(i32 noundef %12, ptr noundef nonnull %4, ptr noundef nonnull %6, i64 noundef 4096, ptr noundef nonnull %5) #10
  br label %14

14:                                               ; preds = %11, %9
  %15 = phi i32 [ %10, %9 ], [ %13, %11 ]
  %16 = icmp ne i32 %15, 0
  %17 = load ptr, ptr %5, align 8
  %18 = icmp eq ptr %17, null
  %19 = select i1 %16, i1 true, i1 %18
  br i1 %19, label %29, label %20

20:                                               ; preds = %14
  %21 = getelementptr inbounds nuw i8, ptr %4, i64 48
  %22 = load ptr, ptr %21, align 8
  %23 = icmp eq ptr %22, null
  br i1 %23, label %29, label %24

24:                                               ; preds = %20
  %25 = call i64 @strlen(ptr noundef nonnull dereferenceable(1) %22) #10
  %26 = icmp slt i64 %25, %2
  br i1 %26, label %27, label %29

27:                                               ; preds = %24
  %28 = add nsw i64 %25, 1
  call void @llvm.memcpy.p0.p0.i64(ptr noundef align 1 %1, ptr noundef nonnull align 1 %22, i64 noundef %28, i1 noundef false) #10
  br label %29

29:                                               ; preds = %27, %24, %20, %14
  %30 = phi i64 [ -1, %14 ], [ -2, %20 ], [ %25, %27 ], [ -1, %24 ]
  call void @llvm.lifetime.end.p0(i64 4096, ptr nonnull %6) #10
  call void @llvm.lifetime.end.p0(i64 8, ptr nonnull %5) #10
  call void @llvm.lifetime.end.p0(i64 72, ptr nonnull %4) #10
  ret i64 %30
}

declare i32 @getpwnam_r(ptr noundef, ptr noundef, ptr noundef, i64 noundef, ptr noundef) local_unnamed_addr

declare i32 @getpwuid_r(i32 noundef, ptr noundef, ptr noundef, i64 noundef, ptr noundef) local_unnamed_addr

declare i32 @getuid() local_unnamed_addr

declare i64 @strlen(ptr noundef captures(none)) local_unnamed_addr #5

define hidden i64 @__jac_executable_path(ptr noundef %0, i64 noundef %1) local_unnamed_addr #0 {
  %3 = alloca i32, align 4
  call void @llvm.lifetime.start.p0(i64 4, ptr nonnull %3) #10
  %4 = trunc i64 %1 to i32
  store i32 %4, ptr %3, align 4
  %5 = call i32 @_NSGetExecutablePath(ptr noundef %0, ptr noundef nonnull %3) #10
  %6 = icmp eq i32 %5, 0
  br i1 %6, label %7, label %9

7:                                                ; preds = %2
  %8 = call i64 @strlen(ptr noundef nonnull dereferenceable(1) %0) #10
  br label %9

9:                                                ; preds = %2, %7
  %10 = phi i64 [ %8, %7 ], [ -1, %2 ]
  call void @llvm.lifetime.end.p0(i64 4, ptr nonnull %3) #10
  ret i64 %10
}

declare i32 @_NSGetExecutablePath(ptr noundef, ptr noundef) local_unnamed_addr

define hidden range(i64 -1, 49) i64 @__jac_addrinfo_layout(i32 noundef %0) local_unnamed_addr #3 {
  %2 = icmp ult i32 %0, 5
  br i1 %2, label %3, label %7

3:                                                ; preds = %1
  %4 = zext nneg i32 %0 to i64
  %5 = getelementptr inbounds nuw [5 x i64], ptr @switch.table.__jac_addrinfo_layout, i64 0, i64 %4
  %6 = load i64, ptr %5, align 8
  br label %7

7:                                                ; preds = %1, %3
  %8 = phi i64 [ %6, %3 ], [ -1, %1 ]
  ret i64 %8
}

define hidden range(i32 0, 256) i32 @__jac_sockaddr_family(ptr noundef readonly captures(none) %0) local_unnamed_addr #6 {
  %2 = getelementptr inbounds nuw i8, ptr %0, i64 1
  %3 = load i8, ptr %2, align 1
  %4 = zext i8 %3 to i32
  ret i32 %4
}

define hidden range(i64 -1, 17) i64 @__jac_clock_id(i32 noundef %0) local_unnamed_addr #3 {
  %2 = icmp ult i32 %0, 6
  br i1 %2, label %3, label %7

3:                                                ; preds = %1
  %4 = zext nneg i32 %0 to i64
  %5 = getelementptr inbounds nuw [6 x i64], ptr @switch.table.__jac_clock_id, i64 0, i64 %4
  %6 = load i64, ptr %5, align 8
  br label %7

7:                                                ; preds = %1, %3
  %8 = phi i64 [ %6, %3 ], [ -1, %1 ]
  ret i64 %8
}

define hidden i32 @__jac_sleep_ns(i64 noundef %0) local_unnamed_addr #0 {
  %2 = alloca %struct.timespec, align 8
  %3 = alloca %struct.timespec, align 8
  call void @llvm.lifetime.start.p0(i64 16, ptr nonnull %2) #10
  %4 = sdiv i64 %0, 1000000000
  store i64 %4, ptr %2, align 8
  %5 = getelementptr inbounds nuw i8, ptr %2, i64 8
  %6 = mul i64 %4, 1000000000
  %7 = sub i64 %0, %6
  store i64 %7, ptr %5, align 8
  call void @llvm.lifetime.start.p0(i64 16, ptr nonnull %3) #10
  %8 = call i32 @"\01_nanosleep"(ptr noundef nonnull %2, ptr noundef nonnull %3) #10
  %9 = icmp eq i32 %8, 0
  br i1 %9, label %20, label %10

10:                                               ; preds = %1, %17
  %11 = call ptr @__error() #10
  %12 = load i32, ptr %11, align 4
  %13 = icmp eq i32 %12, 4
  br i1 %13, label %17, label %14

14:                                               ; preds = %10
  %15 = call ptr @__error() #10
  %16 = load i32, ptr %15, align 4
  br label %20

17:                                               ; preds = %10
  call void @llvm.memcpy.p0.p0.i64(ptr noundef nonnull align 8 dereferenceable(16) %2, ptr noundef nonnull align 8 dereferenceable(16) %3, i64 16, i1 false)
  %18 = call i32 @"\01_nanosleep"(ptr noundef nonnull %2, ptr noundef nonnull %3) #10
  %19 = icmp eq i32 %18, 0
  br i1 %19, label %20, label %10

20:                                               ; preds = %17, %1, %14
  %21 = phi i32 [ %16, %14 ], [ 0, %1 ], [ 0, %17 ]
  call void @llvm.lifetime.end.p0(i64 16, ptr nonnull %3) #10
  call void @llvm.lifetime.end.p0(i64 16, ptr nonnull %2) #10
  ret i32 %21
}

declare i32 @"\01_nanosleep"(ptr noundef, ptr noundef) local_unnamed_addr

declare void @llvm.memcpy.p0.p0.i64(ptr noalias writeonly captures(none), ptr noalias readonly captures(none), i64, i1 immarg) #7

define hidden i64 @__jac_malloc_size(ptr noundef %0) local_unnamed_addr #0 {
  %2 = tail call i64 @malloc_size(ptr noundef %0) #10
  ret i64 %2
}

declare i64 @malloc_size(ptr noundef) local_unnamed_addr

define hidden noundef double @__jac_fmadd(double noundef %0, double noundef %1, double noundef %2) local_unnamed_addr #3 {
  %4 = tail call double @llvm.fma.f64(double %0, double %1, double %2)
  ret double %4
}

declare double @llvm.fma.f64(double, double, double) #8

define hidden ptr @__jac_va_list(ptr noundef readonly captures(none) %0) local_unnamed_addr #6 {
  %2 = load ptr, ptr %0, align 8
  ret ptr %2
}

define hidden i64 @__jac_va_i64(ptr noundef captures(none) %0) local_unnamed_addr #9 {
  %2 = va_arg ptr %0, i64
  ret i64 %2
}

define hidden double @__jac_va_f64(ptr noundef captures(none) %0) local_unnamed_addr #9 {
  %2 = va_arg ptr %0, double
  ret double %2
}

attributes #0 = { nounwind uwtable(sync) }
attributes #2 = { mustprogress nofree norecurse nosync nounwind willreturn memory(read, argmem: none, inaccessiblemem: none) uwtable(sync) }
attributes #3 = { mustprogress nofree norecurse nosync nounwind willreturn memory(none) uwtable(sync) }
attributes #4 = { mustprogress nocallback nofree nosync nounwind willreturn memory(argmem: readwrite) }
attributes #5 = { mustprogress nocallback nofree nounwind willreturn memory(argmem: read) }
attributes #6 = { mustprogress nofree norecurse nosync nounwind willreturn memory(argmem: read) uwtable(sync) }
attributes #7 = { mustprogress nocallback nofree nounwind willreturn memory(argmem: readwrite) }
attributes #8 = { mustprogress nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #9 = { mustprogress nofree norecurse nosync nounwind willreturn memory(argmem: readwrite) uwtable(sync) }
attributes #10 = { nounwind }
""",
     POSIX_FLOOR_IR_MACOS_X86_64: str = r"""
%struct.stat = type { i32, i16, i16, i64, i32, i32, i32, %struct.timespec, %struct.timespec, %struct.timespec, %struct.timespec, i64, i64, i32, i32, i32, i32, [2 x i64] }
%struct.timespec = type { i64, i64 }
%struct.passwd = type { ptr, ptr, i32, i32, i64, ptr, ptr, ptr, ptr, i64 }

@__stdinp = external local_unnamed_addr global ptr, align 8
@__stdoutp = external local_unnamed_addr global ptr, align 8
@__stderrp = external local_unnamed_addr global ptr, align 8
@switch.table.__jac_addrinfo_layout = private unnamed_addr constant [5 x i64] [i64 16, i64 32, i64 40, i64 48, i64 30], align 8
@switch.table.__jac_clock_id = private unnamed_addr constant [6 x i64] [i64 0, i64 6, i64 12, i64 16, i64 4, i64 8], align 8

define hidden ptr @__jac_errno() local_unnamed_addr #0 {
  %1 = tail call ptr @__error() #9
  ret ptr %1
}

declare ptr @__error() local_unnamed_addr

define hidden ptr @__jac_stdio(i32 noundef %0) local_unnamed_addr #2 {
  %2 = icmp eq i32 %0, 1
  %3 = icmp eq i32 %0, 0
  %4 = load ptr, ptr @__stdinp, align 8
  %5 = load ptr, ptr @__stdoutp, align 8
  %6 = load ptr, ptr @__stderrp, align 8
  %7 = select i1 %2, ptr %5, ptr %6
  %8 = select i1 %3, ptr %4, ptr %7
  ret ptr %8
}

define hidden noundef i32 @__jac_platform_id() local_unnamed_addr #3 {
  ret i32 1
}

define hidden range(i32 -1, 1) i32 @__jac_stat(ptr noundef %0, ptr noundef writeonly captures(none) %1) local_unnamed_addr #0 {
  %3 = alloca %struct.stat, align 8
  call void @llvm.lifetime.start.p0(i64 144, ptr nonnull %3) #9
  %4 = call i32 @"\01_stat$INODE64"(ptr noundef %0, ptr noundef nonnull %3) #9
  %5 = icmp eq i32 %4, 0
  br i1 %5, label %6, label %16

6:                                                ; preds = %2
  %7 = getelementptr inbounds nuw i8, ptr %3, i64 48
  %8 = getelementptr inbounds nuw i8, ptr %1, i64 16
  %9 = load <2 x i64>, ptr %7, align 8
  store <2 x i64> %9, ptr %8, align 8
  %10 = getelementptr inbounds nuw i8, ptr %3, i64 4
  %11 = load i16, ptr %10, align 4
  %12 = zext i16 %11 to i64
  store i64 %12, ptr %1, align 8
  %13 = getelementptr inbounds nuw i8, ptr %3, i64 96
  %14 = load i64, ptr %13, align 8
  %15 = getelementptr inbounds nuw i8, ptr %1, i64 8
  store i64 %14, ptr %15, align 8
  br label %16

16:                                               ; preds = %2, %6
  %17 = phi i32 [ 0, %6 ], [ -1, %2 ]
  call void @llvm.lifetime.end.p0(i64 144, ptr nonnull %3) #9
  ret i32 %17
}

declare void @llvm.lifetime.start.p0(i64 immarg, ptr captures(none)) #4

declare i32 @"\01_stat$INODE64"(ptr noundef, ptr noundef) local_unnamed_addr

declare void @llvm.lifetime.end.p0(i64 immarg, ptr captures(none)) #4

define hidden ptr @__jac_opendir(ptr noundef %0) local_unnamed_addr #0 {
  %2 = tail call ptr @"\01_opendir$INODE64"(ptr noundef %0) #9
  ret ptr %2
}

declare ptr @"\01_opendir$INODE64"(ptr noundef) local_unnamed_addr

define hidden ptr @__jac_readdir(ptr noundef %0) local_unnamed_addr #0 {
  %2 = tail call ptr @"\01_readdir$INODE64"(ptr noundef %0) #9
  ret ptr %2
}

declare ptr @"\01_readdir$INODE64"(ptr noundef) local_unnamed_addr

define hidden i32 @__jac_closedir(ptr noundef %0) local_unnamed_addr #0 {
  %2 = tail call i32 @"\01_closedir"(ptr noundef %0) #9
  ret i32 %2
}

declare i32 @"\01_closedir"(ptr noundef) local_unnamed_addr

define hidden nonnull ptr @__jac_dirent_name(ptr noundef readnone captures(ret: address, provenance) %0) local_unnamed_addr #3 {
  %2 = getelementptr inbounds nuw i8, ptr %0, i64 21
  ret ptr %2
}

define hidden noundef i32 @__jac_at_fdcwd() local_unnamed_addr #3 {
  ret i32 -2
}

define hidden range(i64 -9223372036854775808, 9223372036854775807) i64 @__jac_home_dir(ptr noundef %0, ptr noundef %1, i64 noundef %2) local_unnamed_addr #0 {
  %4 = alloca %struct.passwd, align 8
  %5 = alloca ptr, align 8
  %6 = alloca [4096 x i8], align 16
  call void @llvm.lifetime.start.p0(i64 72, ptr nonnull %4) #9
  call void @llvm.lifetime.start.p0(i64 8, ptr nonnull %5) #9
  store ptr null, ptr %5, align 8
  call void @llvm.lifetime.start.p0(i64 4096, ptr nonnull %6) #9
  %7 = load i8, ptr %0, align 1
  %8 = icmp eq i8 %7, 0
  br i1 %8, label %11, label %9

9:                                                ; preds = %3
  %10 = call i32 @getpwnam_r(ptr noundef nonnull %0, ptr noundef nonnull %4, ptr noundef nonnull %6, i64 noundef 4096, ptr noundef nonnull %5) #9
  br label %14

11:                                               ; preds = %3
  %12 = tail call i32 @getuid() #9
  %13 = call i32 @getpwuid_r(i32 noundef %12, ptr noundef nonnull %4, ptr noundef nonnull %6, i64 noundef 4096, ptr noundef nonnull %5) #9
  br label %14

14:                                               ; preds = %11, %9
  %15 = phi i32 [ %10, %9 ], [ %13, %11 ]
  %16 = icmp ne i32 %15, 0
  %17 = load ptr, ptr %5, align 8
  %18 = icmp eq ptr %17, null
  %19 = select i1 %16, i1 true, i1 %18
  br i1 %19, label %29, label %20

20:                                               ; preds = %14
  %21 = getelementptr inbounds nuw i8, ptr %4, i64 48
  %22 = load ptr, ptr %21, align 8
  %23 = icmp eq ptr %22, null
  br i1 %23, label %29, label %24

24:                                               ; preds = %20
  %25 = call i64 @strlen(ptr noundef nonnull dereferenceable(1) %22) #9
  %26 = icmp slt i64 %25, %2
  br i1 %26, label %27, label %29

27:                                               ; preds = %24
  %28 = add nsw i64 %25, 1
  call void @llvm.memcpy.p0.p0.i64(ptr noundef align 1 %1, ptr noundef nonnull align 1 %22, i64 noundef %28, i1 noundef false) #9
  br label %29

29:                                               ; preds = %27, %24, %20, %14
  %30 = phi i64 [ -1, %14 ], [ -2, %20 ], [ %25, %27 ], [ -1, %24 ]
  call void @llvm.lifetime.end.p0(i64 4096, ptr nonnull %6) #9
  call void @llvm.lifetime.end.p0(i64 8, ptr nonnull %5) #9
  call void @llvm.lifetime.end.p0(i64 72, ptr nonnull %4) #9
  ret i64 %30
}

declare i32 @getpwnam_r(ptr noundef, ptr noundef, ptr noundef, i64 noundef, ptr noundef) local_unnamed_addr

declare i32 @getpwuid_r(i32 noundef, ptr noundef, ptr noundef, i64 noundef, ptr noundef) local_unnamed_addr

declare i32 @getuid() local_unnamed_addr

declare i64 @strlen(ptr noundef captures(none)) local_unnamed_addr #5

define hidden i64 @__jac_executable_path(ptr noundef %0, i64 noundef %1) local_unnamed_addr #0 {
  %3 = alloca i32, align 4
  call void @llvm.lifetime.start.p0(i64 4, ptr nonnull %3) #9
  %4 = trunc i64 %1 to i32
  store i32 %4, ptr %3, align 4
  %5 = call i32 @_NSGetExecutablePath(ptr noundef %0, ptr noundef nonnull %3) #9
  %6 = icmp eq i32 %5, 0
  br i1 %6, label %7, label %9

7:                                                ; preds = %2
  %8 = call i64 @strlen(ptr noundef nonnull dereferenceable(1) %0) #9
  br label %9

9:                                                ; preds = %2, %7
  %10 = phi i64 [ %8, %7 ], [ -1, %2 ]
  call void @llvm.lifetime.end.p0(i64 4, ptr nonnull %3) #9
  ret i64 %10
}

declare i32 @_NSGetExecutablePath(ptr noundef, ptr noundef) local_unnamed_addr

define hidden range(i64 -1, 49) i64 @__jac_addrinfo_layout(i32 noundef %0) local_unnamed_addr #3 {
  %2 = icmp ult i32 %0, 5
  br i1 %2, label %3, label %7

3:                                                ; preds = %1
  %4 = zext nneg i32 %0 to i64
  %5 = getelementptr inbounds nuw [5 x i64], ptr @switch.table.__jac_addrinfo_layout, i64 0, i64 %4
  %6 = load i64, ptr %5, align 8
  br label %7

7:                                                ; preds = %1, %3
  %8 = phi i64 [ %6, %3 ], [ -1, %1 ]
  ret i64 %8
}

define hidden range(i32 0, 256) i32 @__jac_sockaddr_family(ptr noundef readonly captures(none) %0) local_unnamed_addr #6 {
  %2 = getelementptr inbounds nuw i8, ptr %0, i64 1
  %3 = load i8, ptr %2, align 1
  %4 = zext i8 %3 to i32
  ret i32 %4
}

define hidden range(i64 -1, 17) i64 @__jac_clock_id(i32 noundef %0) local_unnamed_addr #3 {
  %2 = icmp ult i32 %0, 6
  br i1 %2, label %3, label %7

3:                                                ; preds = %1
  %4 = zext nneg i32 %0 to i64
  %5 = getelementptr inbounds nuw [6 x i64], ptr @switch.table.__jac_clock_id, i64 0, i64 %4
  %6 = load i64, ptr %5, align 8
  br label %7

7:                                                ; preds = %1, %3
  %8 = phi i64 [ %6, %3 ], [ -1, %1 ]
  ret i64 %8
}

define hidden i32 @__jac_sleep_ns(i64 noundef %0) local_unnamed_addr #0 {
  %2 = alloca %struct.timespec, align 8
  %3 = alloca %struct.timespec, align 8
  call void @llvm.lifetime.start.p0(i64 16, ptr nonnull %2) #9
  %4 = sdiv i64 %0, 1000000000
  store i64 %4, ptr %2, align 8
  %5 = getelementptr inbounds nuw i8, ptr %2, i64 8
  %6 = srem i64 %0, 1000000000
  store i64 %6, ptr %5, align 8
  call void @llvm.lifetime.start.p0(i64 16, ptr nonnull %3) #9
  %7 = call i32 @"\01_nanosleep"(ptr noundef nonnull %2, ptr noundef nonnull %3) #9
  %8 = icmp eq i32 %7, 0
  br i1 %8, label %19, label %9

9:                                                ; preds = %1, %16
  %10 = call ptr @__error() #9
  %11 = load i32, ptr %10, align 4
  %12 = icmp eq i32 %11, 4
  br i1 %12, label %16, label %13

13:                                               ; preds = %9
  %14 = call ptr @__error() #9
  %15 = load i32, ptr %14, align 4
  br label %19

16:                                               ; preds = %9
  call void @llvm.memcpy.p0.p0.i64(ptr noundef nonnull align 8 dereferenceable(16) %2, ptr noundef nonnull align 8 dereferenceable(16) %3, i64 16, i1 false)
  %17 = call i32 @"\01_nanosleep"(ptr noundef nonnull %2, ptr noundef nonnull %3) #9
  %18 = icmp eq i32 %17, 0
  br i1 %18, label %19, label %9

19:                                               ; preds = %16, %1, %13
  %20 = phi i32 [ %15, %13 ], [ 0, %1 ], [ 0, %16 ]
  call void @llvm.lifetime.end.p0(i64 16, ptr nonnull %3) #9
  call void @llvm.lifetime.end.p0(i64 16, ptr nonnull %2) #9
  ret i32 %20
}

declare i32 @"\01_nanosleep"(ptr noundef, ptr noundef) local_unnamed_addr

declare void @llvm.memcpy.p0.p0.i64(ptr noalias writeonly captures(none), ptr noalias readonly captures(none), i64, i1 immarg) #7

define hidden i64 @__jac_malloc_size(ptr noundef %0) local_unnamed_addr #0 {
  %2 = tail call i64 @malloc_size(ptr noundef %0) #9
  ret i64 %2
}

declare i64 @malloc_size(ptr noundef) local_unnamed_addr

define hidden noundef double @__jac_fmadd(double noundef %0, double noundef %1, double noundef %2) local_unnamed_addr #3 {
  %4 = fmul double %0, %1
  %5 = fadd double %4, %2
  ret double %5
}

define hidden noundef ptr @__jac_va_list(ptr noundef readnone returned captures(ret: address, provenance) %0) local_unnamed_addr #3 {
  ret ptr %0
}

define hidden i64 @__jac_va_i64(ptr noundef readonly captures(none) %0) local_unnamed_addr #8 {
  %2 = load ptr, ptr %0, align 8
  %3 = load i32, ptr %2, align 8
  %4 = icmp ult i32 %3, 41
  br i1 %4, label %5, label %11

5:                                                ; preds = %1
  %6 = getelementptr inbounds nuw i8, ptr %2, i64 16
  %7 = load ptr, ptr %6, align 8
  %8 = zext nneg i32 %3 to i64
  %9 = getelementptr i8, ptr %7, i64 %8
  %10 = add nuw nsw i32 %3, 8
  store i32 %10, ptr %2, align 8
  br label %15

11:                                               ; preds = %1
  %12 = getelementptr inbounds nuw i8, ptr %2, i64 8
  %13 = load ptr, ptr %12, align 8
  %14 = getelementptr i8, ptr %13, i64 8
  store ptr %14, ptr %12, align 8
  br label %15

15:                                               ; preds = %11, %5
  %16 = phi ptr [ %9, %5 ], [ %13, %11 ]
  %17 = load i64, ptr %16, align 8
  ret i64 %17
}

define hidden double @__jac_va_f64(ptr noundef readonly captures(none) %0) local_unnamed_addr #8 {
  %2 = load ptr, ptr %0, align 8
  %3 = getelementptr inbounds nuw i8, ptr %2, i64 4
  %4 = load i32, ptr %3, align 4
  %5 = icmp ult i32 %4, 161
  br i1 %5, label %6, label %12

6:                                                ; preds = %1
  %7 = getelementptr inbounds nuw i8, ptr %2, i64 16
  %8 = load ptr, ptr %7, align 8
  %9 = zext nneg i32 %4 to i64
  %10 = getelementptr i8, ptr %8, i64 %9
  %11 = add nuw nsw i32 %4, 16
  store i32 %11, ptr %3, align 4
  br label %16

12:                                               ; preds = %1
  %13 = getelementptr inbounds nuw i8, ptr %2, i64 8
  %14 = load ptr, ptr %13, align 8
  %15 = getelementptr i8, ptr %14, i64 8
  store ptr %15, ptr %13, align 8
  br label %16

16:                                               ; preds = %12, %6
  %17 = phi ptr [ %10, %6 ], [ %14, %12 ]
  %18 = load double, ptr %17, align 8
  ret double %18
}

attributes #0 = { nounwind uwtable(sync) }
attributes #2 = { mustprogress nofree norecurse nosync nounwind willreturn memory(read, argmem: none, inaccessiblemem: none) uwtable(sync) }
attributes #3 = { mustprogress nofree norecurse nosync nounwind willreturn memory(none) uwtable(sync) }
attributes #4 = { mustprogress nocallback nofree nosync nounwind willreturn memory(argmem: readwrite) }
attributes #5 = { mustprogress nocallback nofree nounwind willreturn memory(argmem: read) }
attributes #6 = { mustprogress nofree norecurse nosync nounwind willreturn memory(argmem: read) uwtable(sync) }
attributes #7 = { mustprogress nocallback nofree nounwind willreturn memory(argmem: readwrite) }
attributes #8 = { mustprogress nofree norecurse nosync nounwind willreturn memory(readwrite, inaccessiblemem: none) uwtable(sync) }
attributes #9 = { nounwind }
""";
