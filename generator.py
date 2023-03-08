import onnx

def get_operators(model_file):
    model = onnx.load(model_file)
    return [node.op_type for node in model.graph.node]
    
operators = get_operators('model.onnx')
nodupe = []
for x in operators:
    if x not in nodupe:
       nodupe.append(x)

def op_pick(n, ops):
    print(f"#ifndef __DEFAULT_H__")
    print(f"#define __DEFAULT_H__")
    print(f"")
    print(f"#ifdef __cplusplus")
    print("extern \"C\" {")
    print(f"#endif")
    print(f"")
    print(f"#include <onnx.h>")
    print(f"void * resolver_default_create(void);")
    print(f"void resolver_default_destroy(void * rctx);")

    op_list = ops
    for i in range(n):
        print(f"void resolver_default_op_{op_list[i]}(struct onnx_node_t * n);")
    print(f"extern struct onnx_resolver_t resolver_default;")
    print(f"#ifdef __cplusplus")
    print("}")
    print(f"#endif")
    print(f"#endif")
    
    op_pick(len(nodupe), nodupe)
