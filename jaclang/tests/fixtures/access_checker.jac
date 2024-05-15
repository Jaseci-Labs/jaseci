obj :priv BankAccount {
    has account_no: int;
    can register() {
        print(f"{self.account_no} has been registered.");
    }
}
can :priv privmethod() {
    return "private method";
}
can :priv overide_check() {
    return "inside access_check";
}
glob :priv b=1;
glob :priv p=0;
with entry {
    public = BankAccount(123);
    public.register();
    privmethod();
}
