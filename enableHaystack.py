def enableHaystack(document_store):
    from haystack import Pipeline
    from haystack.nodes import TextConverter, PreProcessor
    
    indexing_pipeline = Pipeline()
    text_converter = TextConverter()
    preprocessor = PreProcessor(
        clean_whitespace=True,
        clean_header_footer=True,
        clean_empty_lines=True,
        split_by="word",
        split_length=200,
        split_overlap=20,
        split_respect_sentence_boundary=True,
    )

    indexing_pipeline.add_node(component=text_converter, name="TextConverter", inputs=["File"])
    indexing_pipeline.add_node(component=preprocessor, name="PreProcessor", inputs=["TextConverter"])
    indexing_pipeline.add_node(component=document_store, name="DocumentStore", inputs=["PreProcessor"])    
    
    from haystack.nodes import BM25Retriever
    # from haystack.nodes import FARMReader
    from haystack.nodes import TransformersReader
    retriever = BM25Retriever(document_store=document_store)
    reader = TransformersReader(model_name_or_path="deepset/minilm-uncased-squad2", use_gpu=True)    
    # reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)
    # reader = FARMReader(model_name_or_path="ahotrod/albert_xxlargev1_squad2_512", use_gpu=True)

    querying_pipeline = Pipeline()
    querying_pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
    querying_pipeline.add_node(component=reader, name="Reader", inputs=["Retriever"])    
    
    return [indexing_pipeline, TransformersReader, querying_pipeline]