

cdef extern from *:
    """
    //preprocessor creates needed struct-type and all function definitions

    //set with keys of type int64 -> resulting typename: kh_int64set_t;
    KHASH_INIT(int64set, int64_t, char, 0, kh_int64_hash_func, kh_int64_hash_equal)

    //Generated code:
    /*
        typedef struct kh_int64set_s { 
            khint_t n_buckets, size, n_occupied, upper_bound; 
            khint32_t *flags; 
            int64_t *keys; 
            char *vals; 
        } kh_int64set_t; 



        static inline __attribute__ ((__unused__)) kh_int64set_t *kh_init_int64set(void) { 
            return (kh_int64set_t*)calloc(1,sizeof(kh_int64set_t)); 
        } 


        static inline __attribute__ ((__unused__)) void kh_destroy_int64set(kh_int64set_t *h) { 
            if (h) { 
                free((void *)h->keys); 
                free(h->flags); 
                free((void *)h->vals); 
                free(h); 
            } 
        } 


        static inline __attribute__ ((__unused__)) void kh_clear_int64set(kh_int64set_t *h) { 
            if (h && h->flags) { 
                memset(h->flags, 0xaa, ((h->n_buckets) < 16? 1 : (h->n_buckets)>>4) * sizeof(khint32_t)); h->size = h->n_occupied = 0; 
            }
        } 



        static inline __attribute__ ((__unused__)) khint_t kh_get_int64set(const kh_int64set_t *h, khint64_t key) { 
            if (h->n_buckets) { 
                khint_t k, i, last, mask, step = 0; 
                mask = h->n_buckets - 1; 
                k = (khint32_t)((key)>>33^(key)^(key)<<11); 
                i = k & mask; 
                last = i; 
                while (!((h->flags[i>>4]>>((i&0xfU)<<1))&2) && (((h->flags[i>>4]>>((i&0xfU)<<1))&1) || !((h->keys[i]) == (key)))) { 
                    i = (i + (++step)) & mask; 
                    if (i == last) 
                        return h->n_buckets; 
                } 
                return ((h->flags[i>>4]>>((i&0xfU)<<1))&3)? h->n_buckets : i; 
            } 
            else return 0; 
        } 

        S

        static inline __attribute__ ((__unused__)) int kh_resize_int64set(kh_int64set_t *h, khint_t new_n_buckets) { 
            khint32_t *new_flags = 0;
            khint_t j = 1; 
            { 
                (--(new_n_buckets), (new_n_buckets)|=(new_n_buckets)>>1, (new_n_buckets)|=(new_n_buckets)>>2, (new_n_buckets)|=(new_n_buckets)>>4, (new_n_buckets)|=(new_n_buckets)>>8, (new_n_buckets)|=(new_n_buckets)>>16, ++(new_n_buckets)); 
                if (new_n_buckets < 4) 
                    new_n_buckets = 4; 
                if (h->size >= (khint_t)
                    (new_n_buckets * __ac_HASH_UPPER + 0.5)) j = 0; 
                else { 
                    new_flags = (khint32_t*)malloc(((new_n_buckets) < 16? 1 : (new_n_buckets)>>4) * sizeof(khint32_t)); 
                    if (!new_flags) 
                        return -1; 
                    memset(new_flags, 0xaa, ((new_n_buckets) < 16? 1 : (new_n_buckets)>>4) * sizeof(khint32_t)); 
                    if (h->n_buckets < new_n_buckets) { 
                        khint64_t *new_keys = (khint64_t*)realloc((void *)h->keys,new_n_buckets * sizeof(khint64_t)); 
                        if (!new_keys) { 
                            free(new_flags); 
                            return -1; 
                        } 
                        h->keys = new_keys; 
                        if (0) { 
                            char *new_vals = (char*)realloc((void *)h->vals,new_n_buckets * sizeof(char)); 
                            if (!new_vals) { 
                                free(new_flags); 
                                return -1; 
                            } 
                            h->vals = new_vals; 
                        } 
                    } 
                } 
            } 
            if (j) { 
                for (j = 0; j != h->n_buckets; ++j) { 
                    if (((h->flags[j>>4]>>((j&0xfU)<<1))&3) == 0) { 
                        khint64_t key = h->keys[j]; 
                        char val; 
                        khint_t new_mask; 
                        new_mask = new_n_buckets - 1; 
                        if (0) 
                            val = h->vals[j]; 
                        (h->flags[j>>4]|=1ul<<((j&0xfU)<<1)); 
                        while (1) { 
                            khint_t k, i, step = 0; 
                            k = (khint32_t)((key)>>33^(key)^(key)<<11); 
                            i = k & new_mask; 
                            while (!((new_flags[i>>4]>>((i&0xfU)<<1))&2)) 
                                i = (i + (++step)) & new_mask; 
                            (new_flags[i>>4]&=~(2ul<<((i&0xfU)<<1))); 
                            if (i < h->n_buckets && ((h->flags[i>>4]>>((i&0xfU)<<1))&3) == 0) {
                                { 
                                    khint64_t tmp = h->keys[i]; h->keys[i] = key; key = tmp; 
                                } 
                                if (0) { 
                                    char tmp = h->vals[i]; 
                                    h->vals[i] = val; 
                                    val = tmp; 
                                } 
                                (h->flags[i>>4]|=1ul<<((i&0xfU)<<1)); 
                            } 
                            else { 
                                h->keys[i] = key; 
                                if (0) 
                                    h->vals[i] = val; 
                                break; 
                            } 
                        } 
                    } 
                } 
                if (h->n_buckets > new_n_buckets) { 
                    h->keys = (khint64_t*)realloc((void *)h->keys,new_n_buckets * sizeof(khint64_t)); 
                    if (0) 
                        h->vals = (char*)realloc((void *)h->vals,new_n_buckets * sizeof(char)); 
                } 
                free(h->flags); 
                h->flags = new_flags; 
                h->n_buckets = new_n_buckets; 
                h->n_occupied = h->size; 
                h->upper_bound = (khint_t)(h->n_buckets * __ac_HASH_UPPER + 0.5); 
            } 
            return 0; 
        } 


        static inline __attribute__ ((__unused__)) khint_t kh_put_int64set(kh_int64set_t *h, khint64_t key, int *ret) { 
            khint_t x; 
            if (h->n_occupied >= h->upper_bound) { 
                if (h->n_buckets > (h->size<<1)) { 
                    if (kh_resize_int64set(h, h->n_buckets - 1) < 0) { 
                        *ret = -1; 
                        return h->n_buckets; 
                    } 
                } 
                else if (kh_resize_int64set(h, h->n_buckets + 1) < 0) { 
                    *ret = -1; 
                    return h->n_buckets; 
                } 
            } 
            { 
                khint_t k, i, site, last, mask = h->n_buckets - 1, step = 0; 
                x = site = h->n_buckets; 
                k = (khint32_t)((key)>>33^(key)^(key)<<11); 
                i = k & mask; 
                if (((h->flags[i>>4]>>((i&0xfU)<<1))&2)) 
                    x = i; 
                else { 
                    last = i; 
                    while (!((h->flags[i>>4]>>((i&0xfU)<<1))&2) && (((h->flags[i>>4]>>((i&0xfU)<<1))&1) || !((h->keys[i]) == (key)))) { 
                        if (((h->flags[i>>4]>>((i&0xfU)<<1))&1)) 
                            site = i; 
                        i = (i + (++step)) & mask; 
                        if (i == last) { 
                            x = site; 
                            break; 
                        } 
                    } 
                    if (x == h->n_buckets) { 
                        if (((h->flags[i>>4]>>((i&0xfU)<<1))&2) && site != h->n_buckets) 
                            x = site; 
                        else 
                            x = i; 
                    } 
                } 
            } 
            if (((h->flags[x>>4]>>((x&0xfU)<<1))&2)) { 
                h->keys[x] = key; 
                (h->flags[x>>4]&=~(3ul<<((x&0xfU)<<1))); 
                ++h->size; 
                ++h->n_occupied; 
                *ret = 1; 
            } 
            else if (((h->flags[x>>4]>>((x&0xfU)<<1))&1)) { 
                h->keys[x] = key; 
                (h->flags[x>>4]&=~(3ul<<((x&0xfU)<<1))); 
                ++h->size; 
                *ret = 2; 
            } 
            else 
                *ret = 0; 
            return x; 
        } 

        static inline __attribute__ ((__unused__)) void kh_del_int64set(kh_int64set_t *h, khint_t x) { 
            if (x != h->n_buckets && !((h->flags[x>>4]>>((x&0xfU)<<1))&3)) { 
                (h->flags[x>>4]|=1ul<<((x&0xfU)<<1)); 
                --h->size; 
            } 
        }
    */
    """
    pass

