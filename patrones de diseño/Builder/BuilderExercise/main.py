from concrete_builder_product import ConcretePCBuilder

builder  = ConcretePCBuilder()

pc_personalizada = (builder
                    .set_cpu('cjdghgdfg')
                    .set_gpu('gpu icore675')
                    .set_ram('500kllño')
                    .set_storage('500987')
                    .build()
                    )
print(pc_personalizada)