import onnx

def get_operators(model_file):
    model = onnx.load(model_file)
    return [node.op_type for node in model.graph.node]
    
operators = get_operators('model.onnx')
nodupe = []
for x in operators:
    if x not in nodupe:
       nodupe.append(x)

def op_pick_write(n, ops):
    with open('default.h', 'w') as f:
      f.write(f"#ifndef __DEFAULT_H__\n")
      f.write(f"#define __DEFAULT_H__\n")
      f.write(f"\n")
      f.write(f"#ifdef __cplusplus\n")
      f.write("extern \"C\" {\n")
      f.write(f"#endif\n")
      f.write(f"\n")
      f.write(f"#include <onnx.h>\n")
      f.write(f"void * resolver_default_create(void);\n")
      f.write(f"void resolver_default_destroy(void * rctx);\n")

      op_list = ops
      for i in range(n):
          f.write(f"void resolver_default_op_{op_list[i]}(struct onnx_node_t * n);\n")
      f.write(f"extern struct onnx_resolver_t resolver_default;\n")
      f.write(f"#ifdef __cplusplus\n")
      f.write("}\n")
      f.write(f"#endif\n")
      f.write(f"#endif")
    
op_pick_write(len(nodupe), nodupe)
