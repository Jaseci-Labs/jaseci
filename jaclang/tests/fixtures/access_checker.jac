obj :priv BankAccount {
    has account_no: int;
    can register() {
        print(f"{self.account_no} has been registered.");
    }
}
can :priv privmethod() {
    return "private method";
}
glob :priv b=1;
with entry {
    public = BankAccount(123);
    public.register();
    privmethod();
}
