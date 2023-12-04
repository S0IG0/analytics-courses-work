import {useEffect, useRef, MutableRefObject} from "react";


const useScroll = (
        parentRef: MutableRefObject<HTMLElement | null>,
        childRef: MutableRefObject<HTMLElement | null>,
        callback: () => void
    ) => {
        const observer = useRef<IntersectionObserver | undefined>();

        useEffect(() => {
            const options = {
                root: parentRef.current,
                rootMargin: '0px',
                threshold: 0
            };

            observer.current = new IntersectionObserver(([target]) => {
                if (target.isIntersecting) {
                    callback();
                }
            }, options);

            if (childRef.current && observer.current) {
                observer.current.observe(childRef.current);
            }

            return () => {
                if (childRef.current && observer.current) {
                    observer.current.unobserve(childRef.current);
                }
            };
        }, [parentRef, childRef, callback]);
    }
;

export default useScroll;
