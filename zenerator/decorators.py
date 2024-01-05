
def memoize(func):
    # Making this LRU would improve memory 
    def memoize_wrapper(self, *args):
        pos = self.mark()
        memo = self.memos.get(pos)
        if memo is None:
            memo = self.memos[pos] = {}
        key = (func, args)
        if key in memo:
            res, end_pos = memo[key]
            self.reset(end_pos)
        else:
            res = func(self, *args)
            end_pos = self.mark()
            memo[key] = (res, end_pos)
        return res
    return memoize_wrapper

def memoize_left_recur(func):
    # Making this LRU would improve memory 
    def memoize_left_recur_wrapper(self, *args):
        pos = self.mark()
        memo = self.memos.get(pos)
        if memo is None:
            memo = self.memos[pos] = {}
        key = (func, args)
        if key in memo:
            res, end_pos = memo[key]
            self.reset(end_pos)
        else:
            # Prime the cache with a Fail
            memo[key] = last_res, last_pos = None, pos
            #Loop until no longer parse is found
            while True:
                self.reset(pos)
                res = func(self, *args)
                end_pos = self.mark()
                if end_pos <= last_pos:
                    break
                memo[key] = last_res, last_pos = res, end_pos
            res = last_res
            self.reset(last_pos)
        return res
    return memoize_left_recur_wrapper