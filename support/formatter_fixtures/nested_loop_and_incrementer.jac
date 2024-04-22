# find the token to delete
idx = 0;
for token_tup in here.expo_push_tokens {
    if token_tup == self.expo_push_token {
        break;
    }
    idx += 1;
}
here.expo_push_tokens.pop(idx);