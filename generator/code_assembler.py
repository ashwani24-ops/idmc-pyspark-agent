class CodeAssembler:

    @staticmethod
    def assemble(read_code,
                 transformation_code,
                 write_code):

        return "\n\n".join([
            read_code,
            transformation_code,
            write_code
        ])