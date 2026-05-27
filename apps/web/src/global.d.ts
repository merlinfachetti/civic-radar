// In React 19 the JSX namespace lives under `React.JSX` instead of being a
// global. This shim restores the ambient global so existing `JSX.Element`
// annotations keep working in this codebase.
import type { JSX as ReactJSX } from "react";

declare global {
  namespace JSX {
    type Element = ReactJSX.Element;
    type ElementType = ReactJSX.ElementType;
    type ElementClass = ReactJSX.ElementClass;
    type LibraryManagedAttributes<C, P> = ReactJSX.LibraryManagedAttributes<C, P>;
    type IntrinsicAttributes = ReactJSX.IntrinsicAttributes;
    type IntrinsicElements = ReactJSX.IntrinsicElements;
  }
}

export {};
