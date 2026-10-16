graph import {
    bootstrap_manifest --> compiler.driver.jir { COMPILER_DIGEST_ROOTS, COMPILER_IDENTITY_NAME, NATIVE_LOWERED_PATHS, is_native_lowered, is_roster_input }
    bootstrap_manifest --> dist.payload.fsutil.skip_jaclang { is_native_lowered }
    bootstrap_manifest --> dist.precompile_bytecode.find_jac_files { is_native_lowered }
    bootstrap_manifest --> dist.precompile_bytecode.seal_bootstrap { is_native_only, seed_abs_entries }
    bootstrap_manifest --> dist.precompile_bytecode.seal_finalize { is_native_only, is_seed_source }
    bootstrap_manifest --> dist.precompile_bytecode.sealable_sources { is_seed_source }
    bootstrap_manifest --> dist.publish.runtime_vendor._compile_runtime_module { is_seed_source }
    client as _client_pkg --> client.runtime_source.resolve_client_runtime_cl_path;
    client --> client.vite_bundler.ViteBundler.build { ensure_client_deps }
    client as _client_pkg --> project.modresolver._resolve_jac_virtual_module;
    compiler --> cli.commands.analysis.gen_parser { gen_all_parsers }
    comptime --> byllm.cli { name as ct_name }
    comptime --> cli.commands.analysis { name as ct_name }
    comptime --> cli.commands.architecture { name as ct_name }
    comptime --> cli.commands.browse { name as ct_name }
    comptime --> cli.commands.build { name as ct_name }
    comptime --> cli.commands.cache { name as ct_name }
    comptime --> cli.commands.code { name as ct_name }
    comptime --> cli.commands.config { name as ct_name }
    comptime --> cli.commands.db { name as ct_name }
    comptime --> cli.commands.execution { name as ct_name }
    comptime --> cli.commands.fix { name as ct_name }
    comptime --> cli.commands.guide { name as ct_name }
    comptime --> cli.commands.mcp { name as ct_name }
    comptime --> cli.commands.precompile { name as ct_name }
    comptime --> cli.commands.project { name as ct_name }
    comptime --> cli.commands.tools { name as ct_name }
    comptime --> cli.manifest { module_of }
    comptime --> cli.shadcn.cli { name as ct_name }
    comptime --> client.cli { name as ct_name }
    comptime --> client.desktop_config { fields, get_field }
    comptime --> scale.config.base_config { fields, get_field }
    comptime --> scale.deploy.target.kubernetes.kubernetes_config { fields, get_field }
    comptime --> scale.plugin { name as ct_name }
    comptime --> scale.scheduler.scheduler { fields, get_field }
    comptime --> scale.scheduler.scheduler_models { fields }
    comptime --> scale.tests.misc.test_config_loader { fields }
    comptime --> scale.tests.misc.test_config_validation { fields }
    comptime --> server.identity.auth_models { fields }
    jac0 --> dist.precompile_bytecode.seal_bootstrap { compile_jac as jac0_compile, discover_impl_files as jac0_impls }
    jac0 --> dist.publish.runtime_vendor._compile_runtime_module { compile_jac, discover_impl_files }
    jac0core --> compiler.backends.native.kernel_resolve._from_sealed_image { sealed }
    jac0core --> compiler.driver.compiler.JacCompiler._get_precompiled_jir_bytecode { sealed as _sealed }
    jac0core --> compiler.driver.compiler.JacCompiler._sealed_jir_data { sealed as _sealed }
    jac0core --> compiler.driver.compiler.JacCompiler._sealed_native_engine { sealed as _sealed }
    jac0core --> dist.precompile_bytecode { ext_registry }
    jac0core --> dist.seal.make_sealed_image { ext_registry }
    meta_importer --> client.targets.desktop.native.host_boot._ensure_jac_meta_importer { JacMetaImporter }
    project --> cli.commands.native_build.native_build { get_config }
    project --> compiler.backends.native.wasm_build._project_gc_settings { get_config }
    scale as scale_mod --> server.endpoints.pages.register_graph_endpoints.graph_page;
    bootstrap_manifest --> compiler.backends.native.kernel_stage0.running_kernel_target { NATIVE_LOWERED_PATHS, NATIVE_ONLY_DIR_REL, NATIVE_ONLY_REL }
    bootstrap_manifest --> project.compiler_host.ProjectHost.is_native_lowered_source { is_native_lowered }
    bootstrap_manifest --> project.compiler_host.ProjectHost.is_native_only_source { is_native_only }
    bootstrap_manifest --> project.compiler_host.ProjectHost.is_seed_source { is_seed_source }
    bootstrap_manifest --> project.kernel_snapshot.manifest_sets { NATIVE_LOWERED_PATHS, NATIVE_ONLY_DIR_REL, NATIVE_ONLY_REL, SEED_PATHS }
    bootstrap_manifest --> compiler.driver.jir { COMPILER_DIGEST_ROSTER, read_input_rules }
    jac0 --> dist.precompile_bytecode._seal_boot_unit { compile_jac as jac0_compile, discover_impl_files as jac0_impls }
    comptime --> cli.commands.native { name as ct_name }
    jac0core --> artifacts.kit.runtime_floor_root { sealed as sealed_mod }
    jac0core --> artifacts.router._omitted { sealed }
    jac0core --> client.js_runtime.BunArtifact.probe_sealed { sealed }
    jac0core --> client.js_runtime.JsEngineArtifact.probe_sealed { sealed }
    jac0core --> compiler.backends.native.floors.CFloorArtifact.probe_sealed { sealed }
    jac0core --> compiler.backends.native.floors.MuslArtifact.probe_sealed { sealed }
    jac0core --> compiler.backends.native.floors.WasmLibcArtifact.probe_sealed { sealed }
    jac0core --> compiler.backends.native.host_facts.compute_fact { sealed }
    jac0core --> compiler.backends.native.llvm.shim_path.ShimArtifact.probe_sealed { sealed }
    jac0core --> compiler.types.stubcat.locate.StubcatArtifact.probe_sealed { sealed }
    jac0core --> compiler.types.stubcat.locate.TypeshedArtifact.probe_sealed { sealed }
    jac0core --> dist.interpreter.JacPythonArtifact.probe_sealed { sealed }
    jac0core --> dist.precompiled.PrecompiledArtifact.probe_sealed { sealed }
    jac0core --> project.kernel_snapshot.catalog_build_blocker { sealed }
    comptime byllm.cli --> cli.manifest { SPEC_MODEL }
    byllm.config_loader --> byllm.llm { get_byllm_config }
    byllm.config_loader --> byllm.mtir { get_byllm_config }
    byllm.config_loader --> byllm.tests.test_byllm { JacByllmConfig, get_byllm_config, reset_byllm_config }
    byllm.config_loader --> byllm.tests.test_compaction { get_byllm_config, reset_byllm_config }
    byllm.config_loader --> byllm.tests.test_parallel { get_byllm_config, reset_byllm_config }
    byllm.config_loader --> byllm.tests.test_typed_retry { get_byllm_config, reset_byllm_config }
    byllm.config_loader --> byllm.tests.test_usage { JacByllmConfig }
    byllm.config_loader --> runtime.runtime.JacLLM.default_llm { get_byllm_config }
    byllm.exceptions --> byllm.lib { AuthenticationError, ByLLMError, ConfigurationError, FinishToolError, McpError, ModelNotFoundError, OutputConversionError, RateLimitError }
    byllm.exceptions --> byllm.llm { AuthenticationError, CompactionNotEffectiveError, ConfigurationError, FinishToolError, ModelNotFoundError, OutputConversionError, RateLimitError }
    byllm.exceptions --> byllm.mcp { McpError }
    byllm.exceptions --> byllm.mtir { ConfigurationError, OutputConversionError }
    byllm.exceptions --> byllm.schema { ConfigurationError }
    byllm.exceptions --> byllm.tests.test_byllm { AuthenticationError, ConfigurationError, FinishToolError, McpError, ModelNotFoundError, OutputConversionError, RateLimitError }
    byllm.exceptions --> byllm.tests.test_compaction { CompactionNotEffectiveError, ConfigurationError }
    byllm.exceptions --> byllm.tests.test_mockllm { OutputConversionError }
    byllm.exceptions --> byllm.tests.test_streaming { ConfigurationError }
    byllm.exceptions --> byllm.tests.test_tool_arg_streaming { FinishToolError, OutputConversionError }
    byllm.exceptions --> byllm.types { ByLLMError, FinishToolError }
    byllm.exceptions --> runtime.runtime.JacLLM.default_llm { ConfigurationError }
    byllm.lib --> byllm.tests.fixtures.async_by_llm { Model }
    byllm.lib --> byllm.tests.fixtures.basic { MockLLM }
    byllm.lib --> byllm.tests.fixtures.basic_compile { MockLLM }
    byllm.lib --> byllm.tests.fixtures.enum_no_value { Model }
    byllm.lib --> byllm.tests.fixtures.enum_with_semstr { Model }
    byllm.lib --> byllm.tests.fixtures.import_dir.importable_schema { MockLLM }
    byllm.lib --> byllm.tests.fixtures.proj { MockLLM }
    byllm.lib --> byllm.tests.fixtures.scope_dir.module_alpha { MockLLM }
    byllm.lib --> byllm.tests.fixtures.scope_dir.module_beta { MockLLM }
    byllm.lib --> byllm.tests.fixtures.test_schema { Model }
    byllm.lib --> byllm.tests.fixtures.tool_function { MockLLM, MockToolCall }
    byllm.lib --> byllm.tests.fixtures.tool_method { MockLLM, MockToolCall }
    byllm.lib --> byllm.tests.support { MockError, MockLLM, MockRawResponse, MockToolCall }
    byllm.lib --> byllm.tests.test_byllm { Image, MockLLM, Model, ModelPool, Video }
    byllm.lib --> byllm.tests.test_compaction { MockLLM, Model, ModelPool }
    byllm.lib --> byllm.tests.test_conversation { MockLLM }
    byllm.lib --> byllm.tests.test_media { ConfigurationError, Image, MockLLM, Video }
    byllm.lib --> byllm.tests.test_mockllm { MockError, MockLLM, MockRawResponse, MockToolCall, Model, StreamEvent }
    byllm.lib --> byllm.tests.test_model_pool { Model, ModelPool }
    byllm.lib --> byllm.tests.test_parallel { Model }
    byllm.lib --> byllm.tests.test_prompting { MockLLM }
    byllm.lib --> byllm.tests.test_streaming { MockLLM, Model }
    byllm.lib --> byllm.tests.test_tool_arg_streaming { MockLLM, MockRawResponse, MockToolCall }
    byllm.lib --> byllm.tests.test_tools { MockLLM }
    byllm.lib --> byllm.tests.test_truncated_tool_calls { Model }
    byllm.lib --> byllm.tests.test_typed_retry { MockLLM }
    byllm.lib --> byllm.tests.test_usage { MockLLM, Model }
    byllm.lib --> byllm.tests.validate_schema { Model }
    byllm.llm --> byllm.lib { MockLLM, Model, ModelPool }
    byllm.llm --> byllm.tests.fixtures.async_stream_by_llm { BaseLLM }
    byllm.llm --> byllm.tests.support { BaseLLM }
    byllm.llm as _byllm_llm_mod --> byllm.tests.test_byllm;
    byllm.llm --> byllm.tests.test_byllm { _CACHE_CONTROL_EPHEMERAL, _apply_prompt_caching, _is_prompt_caching_eligible }
    byllm.llm as _byllm_llm_mod --> byllm.tests.test_compaction;
    byllm.llm --> byllm.tests.test_compaction { BaseLLM, LocalLLM }
    byllm.llm --> byllm.tests.test_parallel { BaseLLM }
    byllm.llm as _byllm_llm_mod --> byllm.tests.test_telemetry_;
    byllm.llm as _byllm_llm_mod --> byllm.tests.test_tool_arg_streaming;
    byllm.llm as _byllm_llm_mod --> byllm.tests.test_usage;
    byllm.llm --> byllm.visit_routing { BaseLLM }
    byllm.llm --> runtime.runtime.JacLLM.by_operator { BaseLLM }
    byllm.llm --> runtime.runtime.JacLLM.default_llm { Model }
    byllm.local_runtime --> byllm.cli._cmd_model { LOCAL_MODELS, list_local_aliases }
    byllm.local_runtime --> byllm.llm { LOCAL_MODELS, filter_params, list_local_aliases, parse_alias, wrap_tool_call }
    byllm.mcp --> byllm.lib | byllm.tests.test_byllm { McpClient, McpTool }
    byllm.mcp --> byllm.mtir | byllm.types { McpTool }
    byllm.model_cache --> byllm.cli._cmd_model { ensure_model, force_pull, get_cache_dir, is_downloaded, list_downloaded, remove_alias }
    byllm.model_cache --> byllm.llm { ensure_model }
    byllm.mtir --> byllm.lib | byllm.tests.test_telemetry_ { MTIR, MTRuntime }
    byllm.mtir --> byllm.llm { MTRuntime }
    type byllm.mtir --> byllm.telemetry | runtime.runtime { MTRuntime }
    byllm.mtir --> byllm.tests.support { MTRuntime }
    byllm.mtir --> byllm.tests.test_byllm { MTRuntime }
    byllm.mtir --> byllm.tests.test_usage { MTRuntime }
    byllm.mtir --> byllm.visit_routing.route_visit { MTRuntime }
    byllm.mtir --> runtime.runtime.JacLLM.by._decorator._wrapped_caller { MTIR }
    byllm.mtir --> runtime.runtime.JacLLM.get_mtir { MTIR }
    byllm.parallel --> byllm.lib { dispatch_batch, mark_serialize }
    byllm.parallel --> byllm.llm { _PARALLEL_TOOL_HINT, _index_by_identity, dispatch_batch }
    byllm.parallel --> byllm.tests.test_parallel { _PARALLEL_TOOL_HINT, _WORKER_POOL, _index_by_identity, _is_async, dispatch_batch, mark_serialize }
    byllm.schema --> byllm.llm { inject_schema_hint }
    byllm.schema --> byllm.mtir { json_to_instance, type_to_schema }
    byllm.schema as schema --> byllm.tests.test_mtir_integration;
    byllm.schema --> byllm.types { tool_to_schema }
    byllm.telemetry --> byllm.lib { register_agent_callback }
    byllm.telemetry --> byllm.llm { _aggregate_usage, _current_invocation_id, _emit_agent_telemetry }
    byllm.telemetry --> byllm.tests.test_streaming { _current_invocation_id }
    byllm.telemetry --> byllm.tests.test_telemetry_ { _agent_callbacks, _current_invocation_id, _emit_agent_telemetry, register_agent_callback }
    byllm.telemetry --> byllm.tests.test_usage { _agent_callbacks, register_agent_callback }
    byllm.telemetry --> scale.admin.llm_telemetry.JacAPIServerLLMTelemetry.register_llm_telemetry_endpoints { register_agent_callback }
    byllm.tool_protocol --> byllm.llm { coerce_message_dict, inject_tool_hint, recover_tool_calls, response_field }
    byllm.tool_protocol --> byllm.tests.test_byllm { linearize_tool_messages, recover_tool_calls }
    byllm.types --> byllm.lib { Image, IterationAction, IterationContext, Message, MessageRole, MockError, MockRawResponse, MockToolCall, StreamEvent, Tool, ToolCallResultMsg, Video }
    byllm.types --> byllm.llm { CompletionResult, Image, IterationAction, IterationContext, LiteLLMMessage, Message, MessageRole, MockError, MockRawResponse, MockToolCall, StreamEvent, Tool, ToolCall, content_preview, image_resp_kind, reroute_tool_images_to_user_message, response_dict }
    byllm.types --> byllm.mtir { LiteLLMMessage, Media, Message, MessageRole, MessageType, Text, Tool, ToolCallResultMsg, image_resp_kind }
    byllm.types --> byllm.parallel { ToolCallResultMsg, normalize_tool_result }
    byllm.types --> byllm.tests.support { Message, MessageRole, StreamEvent, Tool }
    byllm.types --> byllm.tests.test_byllm { Message, MessageRole, Tool }
    byllm.types --> byllm.tests.test_compaction { MockToolCall }
    byllm.types --> byllm.tests.test_conversation { Message, MessageRole }
    byllm.types --> byllm.tests.test_multimodal_tool_results { Image, Text, ToolCallResultMsg, content_preview, normalize_tool_result, reroute_tool_images_to_user_message }
    byllm.types --> byllm.tests.test_parallel { Message, MessageRole, MockToolCall, Tool }
    byllm.types --> byllm.tests.test_telemetry_ { Message, MessageRole, Text }
    byllm.types --> byllm.tests.test_tools { IterationAction, IterationContext }
    byllm.types --> byllm.tests.test_usage { IterationContext, MockToolCall }
    byllm.types --> byllm.visit_routing.route_visit { Message, MessageRole }
    byllm.visit_routing --> runtime.runtime.JacLLM.by_operator { route_visit }
    byllm.mtir --> byllm.tests.test_mtir_integration { MTIR }
    byllm.exceptions --> byllm.lib { LLMTimeout }
    byllm.exceptions --> byllm.llm { ByLLMError, LLMTimeout }
    byllm.exceptions --> byllm.systemone { OutputConversionError }
    byllm.exceptions --> byllm.tests.test_systemone { AuthenticationError, ByLLMError, ConfigurationError, RateLimitError }
    byllm.exceptions --> byllm.tests.test_timeout { LLMTimeout, RateLimitError }
    byllm.lib --> byllm.tests.test_compaction_budget { MockLLM }
    byllm.lib --> byllm.tests.test_compaction_conversation { MockLLM }
    byllm.lib --> byllm.tests.test_conversation_system_prompt { MockLLM }
    byllm.lib --> byllm.tests.test_systemone { Decision, MockLLM, MockSystemOne, Model }
    byllm.lib --> byllm.tests.test_timeout { Model, ModelPool }
    byllm.llm --> byllm.lib { MockSystemOne, SystemOneModel }
    byllm.llm --> byllm.tests.support { MockSystemOne }
    byllm.llm as _byllm_llm_mod --> byllm.tests.test_compaction_budget;
    byllm.llm --> byllm.tests.test_systemone { SystemOneModel }
    byllm.llm --> byllm.tests.test_timeout { _is_timeout_error, _is_transient_error }
    byllm.mtir --> byllm.systemone { MTRuntime }
    byllm.mtir --> byllm.tests.test_systemone { MTIR, MTRuntime }
    byllm.systemone --> byllm.lib { Decision }
    byllm.systemone --> byllm.llm { Decision, ProviderCaps, SYSTEMONE_PREFIX, SystemOneSpec, assemble, caps_for, distribution, lower, resolve_api_key, resolve_model_name, wrap_result }
    byllm.systemone --> byllm.tests.test_systemone { ROUTE_SELECT_ATTR, assemble, lower, resolve_model_name }
    byllm.systemone --> byllm.visit_routing { ROUTE_SELECT_ATTR }
    byllm.types --> byllm.systemone.build_state { Media }
    byllm.types --> byllm.systemone.lower { image_resp_kind }
    byllm.exceptions --> byllm.lib | byllm.llm { OutputTruncatedError }
    byllm.lib --> byllm.tests.test_tools { MockRawResponse }
    byllm.lib --> byllm.tests.test_truncated_tool_calls { OutputTruncatedError }
    byllm.lib --> byllm.tests.test_usage { OutputTruncatedError }
    byllm.exceptions --> byllm.tests.test_typed_retry { OutputConversionError }
    byllm.lib --> byllm.tests.test_document { Document, MockLLM }
    byllm.schema --> byllm.llm { type_display_name }
    byllm.schema --> byllm.mtir { type_display_name }
    byllm.schema --> byllm.tests.test_byllm { type_display_name }
    byllm.schema --> byllm.types { type_display_name }
    byllm.types --> byllm.lib { Document }
    byllm._optdeps.litellm --> byllm.llm { _disable_debugging, litellm }
    byllm._optdeps.litellm --> byllm.tests.test_telemetry_ { LiteLLMMessage }
    byllm._optdeps.litellm --> byllm.types { LiteLLMMessage }
    byllm._optdeps.loguru --> byllm.llm | byllm.visit_routing { logger }
    byllm._optdeps.openai --> byllm.llm { AsyncOpenAI, OpenAI, openai }
    byllm._optdeps.pillow --> byllm.types { PILImageCls, open_image }
    byllm._optdeps.pydantic --> byllm.schema | byllm.types { TypeAdapter }
    byllm._optdeps.litellm --> byllm.tests.test_timeout { litellm }
    byllm._optdeps.litellm --> byllm.tests.test_compaction_conversation { LiteLLMMessage }
    byllm._optdeps._deferred --> byllm._optdeps.litellm { DeferredClassMeta, DeferredModule, is_installed, when_loaded }
    byllm._optdeps._deferred --> byllm._optdeps.openai { DeferredClassMeta, DeferredModule, is_installed }
    byllm._optdeps.litellm --> byllm.exceptions | byllm.llm { when_litellm_loaded }
    byllm._optdeps.litellm --> scale.admin.llm_telemetry.JacAPIServerLLMTelemetry.register_llm_telemetry_endpoints { HAS_LITELLM, when_litellm_loaded }
    byllm.tests.fixtures --> byllm.tests.test_byllm { python_lib_mode }
    byllm.tests.fixtures --> byllm.tests.test_mtir_integration { python_lib_mode }
    byllm.tests.support --> byllm.tests.test_byllm { FIXTURE_DIR, call as tool_call, capture_logs, capture_loguru, finish, fixture_path, load_fixture, mk_run, prompt_text, say, scripted, text_chunk, tool_names }
    byllm.tests.support --> byllm.tests.test_compaction { call, fail, finish, fixture_path, scripted }
    byllm.tests.support --> byllm.tests.test_conversation { call, finish, say }
    byllm.tests.support --> byllm.tests.test_media { data_url, fixture_path, media_blocks, need, prompt_text, roles, say, user_blocks }
    byllm.tests.support --> byllm.tests.test_model_pool { text_chunk }
    byllm.tests.support --> byllm.tests.test_mtir_integration { fixture_path, load_fixture, need_outside_jaclang }
    byllm.tests.support --> byllm.tests.test_parallel { mk_run }
    byllm.tests.support --> byllm.tests.test_prompting { call, fixture_path, prompt_text, roles, say, tool_names }
    byllm.tests.support --> byllm.tests.test_routing { RoutingLLM, prompt_text, routing_candidates, say }
    byllm.tests.support --> byllm.tests.test_streaming { call, chunk_text, event_types, events_of, fail, finish, mk_run, prompt_text, say, scripted, stream_events }
    byllm.tests.support --> byllm.tests.test_tool_arg_streaming { call, calls, event_types, events_of, fail, mk_run, say }
    byllm.tests.support --> byllm.tests.test_tools { call, finish, prompt_text, say, tool_names }
    byllm.tests.support --> byllm.tests.test_truncated_tool_calls { call, say, scripted }
    byllm.tests.support --> byllm.tests.test_typed_retry { FIXTURE_DIR, fail, prompt_text, say }
    byllm.tests.support --> byllm.tests.test_usage { TOKENS, call, events_of, finish, mk_run, say, scripted }
    byllm.tests.fixtures.agent_graph as ag --> byllm.tests.test_routing;
    byllm.tests.fixtures.agent_graph --> byllm.tests.test_routing { MathAgent, PoemAgent, Team, supervisor }
    byllm.tests.fixtures.routing_graph as rg --> byllm.tests.test_routing;
    byllm.tests.fixtures.routing_graph --> byllm.tests.test_routing { Agent, Hub, Route, collector, leaky, picker, router, stream_router }
    byllm.tests.fixtures.import_dir.importable_schema --> byllm.tests.fixtures.importer_main { get_imported_data }
    byllm.tests.fixtures.scope_dir.module_alpha --> byllm.tests.fixtures.scope_main { process_data as alpha_process }
    byllm.tests.fixtures.scope_dir.module_beta --> byllm.tests.fixtures.scope_main { process_data as beta_process }
    cache.home --> cache.policy { CACHEDIR_TAG }
    cache.home --> cache.registry { CACHEDIR_TAG, cache_home, ensure_cache_dir, ensure_root }
    cache.home --> cli.commands.cache { cache_home }
    cache.locking --> cache.policy { FileLock }
    cache.policy --> cache.registry { CacheEntry, EntryKind, Policy, Retention, SWEEP_SENTINEL, SweepReport, TempLock, TemporaryClaim, dir_size, maybe_sweep_dir, remove_entry, scan_entries, sweep_dir, touch }
    cache.policy --> cli.commands.cache { format_bytes }
    cache.policy --> cli.format_cache { DAY_SECONDS, Policy, SWEEP_INTERVAL_SECONDS, SWEEP_SENTINEL, maybe_sweep_dir }
    cache.policy --> compiler.driver.jir._sweep_once { maybe_sweep_dir }
    cache.policy --> compiler.driver.jir.sweep_stale_generations { sweep_dir }
    cache.registry --> byllm.model_cache.get_cache_dir { bucket }
    cache.registry --> cli.commands.cache { RETIRED, gc, purge, status, unmanaged }
    cache.registry --> compiler.driver.jir._manifest_compiler_digest { bucket, maybe_sweep }
    cache.registry --> compiler.driver.jir._sweep_once { bucket, maybe_sweep }
    cache.registry --> compiler.driver.jir._touch_generation { bucket }
    cache.registry --> compiler.driver.jir.sweep_stale_generations { bucket }
    cache.registry --> compiler.types.stubcat.locate.dev_catalog_path { bucket }
    cache.registry --> dist.fused_binary._runtime_dir_for_key { bucket }
    cache.registry --> dist.jab { bucket, maybe_sweep }
    cache.registry --> scale.injector.binary._fetch_verified_asset { maybe_sweep }
    cache.registry --> scale.injector.binary._scale_cache_root { bucket }
    cache.registry --> toolchains.android { bucket }
    cache.registry --> toolchains.store { bucket, maybe_sweep }
    cache.policy --> cache.registry { KeepMatch }
    cache.registry --> packages.index.Registry._cache_file | packages.sources._mirror_dir | packages.store.materialize | project.package_scope.store_root { bucket }
    cache.registry --> packages.index.fetch_verified { bucket }
    cache.registry --> client.js_runtime.installed_engine_dir { bucket }
    cache.registry --> compiler.types.stubcat.locate.StubcatArtifact.build { maybe_sweep }
    cache.registry --> compiler.types.stubcat.locate.StubcatArtifact.probe_checkout { bucket }
    cache.registry --> data.pg_dist.dist_cache_dir { bucket }
    cache.registry --> server.session.shared_pg_data_dir { bucket }
    cache.registry --> toolchains.tools.ToolArtifact.checkout_path { bucket }
    cli.banners --> server.server.JacAPIServer._ensure_client_bundle { JAC_DISCORD_URL }
    cli.browser_engine --> cli.commands.browse { cmd_click, cmd_close, cmd_console, cmd_eval, cmd_fill, cmd_get, cmd_navigate, cmd_open, cmd_press, cmd_screenshot, cmd_scroll, cmd_sessions, cmd_snapshot, cmd_state, cmd_type, cmd_wait }
    cli.check_report --> cli.commands.analysis { print_failed_summary, print_file_progress, print_final_summary, print_native_coverage, print_placement_report, print_section }
    cli.check_report --> cli.commands.analysis.explain { print_placement_report }
    cli.cli --> cli.cli_boot.start_cli { start_cli as _start_cli }
    cli.cli --> cli.commands.analysis.format { jac_version }
    cli.cli --> cli.commands.project._stamp_jac_version { jac_version }
    cli.cli_boot --> jac0core.cli_boot { start_cli }
    cli.command --> byllm.cli { Arg, ArgKind, CommandSpec }
    cli.command --> cli.commands.analysis { Arg, ArgKind, CommandSpec }
    cli.command --> cli.commands.architecture { Arg, ArgKind, CommandSpec }
    cli.command --> cli.commands.browse { Arg, ArgKind, CommandSpec }
    cli.command --> cli.commands.build { Arg, ArgKind, CommandSpec }
    cli.command --> cli.commands.cache { Arg, ArgKind, CommandSpec }
    cli.command --> cli.commands.code { Arg, ArgKind, CommandSpec }
    cli.command --> cli.commands.config { Arg, ArgKind, CommandSpec }
    cli.command --> cli.commands.db { Arg, ArgKind, CommandSpec }
    cli.command --> cli.commands.execution { Arg, ArgKind, CommandSpec }
    cli.command --> cli.commands.fix { Arg, ArgKind, CommandSpec }
    cli.command --> cli.commands.guide { Arg, ArgKind, CommandSpec }
    cli.command --> cli.commands.mcp | cli.shadcn.cli { Arg, CommandSpec }
    cli.command --> cli.commands.precompile { Arg, ArgKind, CommandSpec }
    cli.command --> cli.commands.project { Arg, ArgKind, CommandSpec }
    cli.command --> cli.commands.tools { Arg, ArgKind, CommandSpec }
    cli.command --> cli.commands.tools._extract_commands { ArgKind }
    cli.command --> cli.dispatch { Arg, ArgKind, CommandSpec, arg_consumes_value }
    cli.command --> cli.executor | cli.manifest_help { CommandSpec }
    cli.command --> cli.executor.CommandExecutor.execute { CommandSpec }
    cli.command --> cli.executor.CommandExecutor.run_handler { CommandSpec }
    cli.command --> cli.manifest { Arg, ArgKind, CommandSpec }
    cli.command --> cli.manifest_parse { Arg, ArgKind, CommandSpec, arg_consumes_value, resolve_arg_typ }
    cli.command --> cli.mcp_manifest.get_command { arg_typ_name }
    cli.command --> client.cli { Arg, ArgKind, CommandSpec }
    cli.command --> scale.plugin { Arg, ArgKind, CommandSpec }
    cli.console --> byllm.cli { console }
    cli.console --> byllm.model_cache._emit { console }
    cli.console --> cli.banners { console }
    cli.console --> cli.check_report.print_diag { console }
    cli.console --> cli.check_report.print_failed_summary { console }
    cli.console --> cli.check_report.print_file_progress { console }
    cli.console --> cli.check_report.print_final_summary { console }
    cli.console --> cli.check_report.print_guide_hint { console }
    cli.console --> cli.check_report.print_native_coverage { console }
    cli.console --> cli.check_report.print_placement_report { console }
    cli.console --> cli.check_report.print_section { console }
    cli.console --> cli.cli.start_cli { console }
    cli.console --> cli.commands.analysis { console }
    cli.console --> cli.commands.analysis.explain { console }
    cli.console --> cli.commands.architecture { console }
    cli.console --> cli.commands.browse { console }
    cli.console --> cli.commands.build { console }
    cli.console --> cli.commands.cache { console }
    cli.console --> cli.commands.cli_helpers { console }
    cli.console --> cli.commands.code { console }
    cli.console --> cli.commands.config { console }
    cli.console --> cli.commands.db { console }
    cli.console --> cli.commands.execution { console, use_line_buffered_output }
    cli.console --> cli.commands.fix { console }
    cli.console --> cli.commands.guide { console }
    cli.console --> cli.commands.native_build { console }
    cli.console --> cli.commands.project { console }
    cli.console --> cli.commands.tools { console }
    cli.console --> cli.commands.transform { console }
    cli.console --> cli.dispatch._apply_profile { console }
    cli.console --> cli.dispatch._exit_on_invalid_jac_toml { console }
    cli.console --> cli.dispatch._exit_on_malformed_jac_toml { console }
    cli.console --> cli.dispatch.run_selected_command { console }
    cli.console --> cli.executor { console }
    cli.console --> cli.manifest_help._use_color { console }
    cli.console --> cli.shadcn.cli._build_shadcn_template_info { console }
    cli.console --> cli.shadcn.cli._shadcn_post_create { console }
    cli.console --> cli.shadcn.cli.retheme { console }
    cli.console --> cli.shadcn.cli.run_shadcn_add { console }
    cli.console --> cli.shadcn.cli.run_shadcn_remove { console }
    cli.console --> cli.shadcn.shadcn_handler { console }
    cli.console --> cli.shadcn.theme_handler { console }
    cli.console --> client.asset_processor { console }
    cli.console --> client.cli._npm_context { console }
    cli.console --> client.cli.run_client_build { console }
    cli.console --> client.cli.run_client_setup { console }
    cli.console --> client.cli.run_client_start { console }
    cli.console --> client.cli.run_npm_add { console }
    cli.console --> client.cli.run_npm_add_global { console }
    cli.console --> client.cli.run_npm_remove { console }
    cli.console --> client.cli.setup { console }
    cli.console --> client.client_deps.prompt_install_client_deps { console }
    cli.console --> client.compiler { console }
    cli.console --> client.config_loader { console }
    cli.console --> client.desktop_config { console }
    cli.console --> client.jac_client_compiler { console }
    cli.console --> client.npm_provider.app_npm_deps._add { console }
    cli.console --> client.plugin_config._load_template { console }
    cli.console --> client.targets.client_dev_common { console }
    cli.console --> client.targets.desktop.cef_shell { console }
    cli.console --> client.targets.desktop.desktop_build { console }
    cli.console --> client.targets.desktop.native.cef.build { console }
    cli.console --> client.targets.desktop.webview_shell { console }
    cli.console --> client.targets.mobile_target { console }
    cli.console --> client.targets.node_tooling_common { console }
    cli.console --> client.targets.pwa_build { console }
    cli.console --> client.targets.react_native.build { console }
    cli.console --> client.targets.react_native.dev { console }
    cli.console --> client.targets.react_native.scaffold { console }
    cli.console --> client.targets.static_target { console }
    cli.console --> client.targets.web_target.WebTarget.dev { console }
    cli.console --> client.vite_bundler { console }
    cli.console --> client.vite_client_bundle { console }
    cli.console --> compiler.backends.native.elf_linker { console }
    cli.console --> compiler.driver.application.prepare_application { console }
    cli.console --> compiler.driver.application.prepare_dynamic_module { console }
    cli.console --> compiler.tools.lang_tools { console }
    cli.console --> dist.precompile_bytecode { console }
    cli.console --> dist.seal { console }
    cli.console --> lsp.server.engine { console }
    cli.console --> lsp.server.server { console }
    cli.console --> project.config.JacConfig._write_toml_text { console }
    cli.console --> project.config._apply_build_section { console }
    cli.console --> project.config._apply_memory_native_placement { console }
    cli.console --> project.config._parse_toml_data { console }
    cli.console --> project.config_schema.report_schema_findings { console }
    cli.console --> project.providers { console }
    cli.console --> project.pyvenv { console }
    cli.console --> project.template_loader { console }
    cli.console --> project.template_registry._register_builtin_client_templates { console }
    cli.console --> project.template_registry._register_builtin_shadcn_template { console }
    type cli.console --> runtime.runtime { JacConsole as ConsoleImpl }
    cli.console --> runtime.runtime.JacBuiltin.get_console { JacConsole }
    cli.console --> scale.deploy.target.factory.ensure_deploy_tooling { console }
    cli.console --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._build_client_bundle { console }
    cli.console --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._install_app_deps { console }
    cli.console --> scale.deploy.target.kubernetes.target.KubernetesTarget._wait_for_fleet_rollout { console }
    cli.console --> scale.deploy.target.kubernetes.utils.kubernetes_utils { console }
    cli.console --> scale.injector.binary_injector.select_injector { console }
    cli.console --> scale.observability.standard_logger { console }
    cli.console --> scale.plugin { console }
    cli.console --> scale.runtime.cli.plan { console }
    cli.console --> scale.runtime.orchestrator.orchestrator { console }
    cli.console --> scale.runtime.realizer.kubernetes_realizer { console }
    cli.console --> scale.utils.vendor_wheels { console }
    cli.console --> server.assembly { console }
    cli.console --> server.hmr { console }
    cli.console --> server.server.JacAPIServer._ensure_client_bundle { console }
    cli.console --> server.server.JacAPIServer.start { console }
    cli.console --> server.server.print_endpoint_docs { console }
    cli.console --> server.watcher { console }
    cli.console --> testing.cl_test_runner { console }
    cli.console --> testing.test { console }
    cli.console --> toolchains.android { console }
    cli.console --> toolchains.host { console }
    cli.console --> toolchains.manager { console }
    cli.console --> toolchains.store { console }
    cli.dispatch --> cli.manifest_route.handle_manifest_route { run_selected_command }
    cli.errmap --> cli.executor.CommandExecutor.execute { humanize_error, show_tracebacks }
    cli.errmap --> scale.tests.server.test_serve { humanize_error }
    cli.executor --> cli.dispatch.run_selected_command { get_executor }
    cli.format_cache --> cli.commands.analysis._format_single_file_worker { FormatCache, canonical_logical_path, config_fingerprint, default_format_cache_dir, frame_unit }
    cli.format_cache --> cli.commands.analysis.format { FORMAT_CACHE_SCHEMA_VERSION, formatter_pipeline_revision }
    cli.guide_store --> cli.check_report.print_guide_hint { guide_for_diagnostic }
    cli.guide_store --> cli.commands.guide { Guide, corpus_blurb, doc_corpora, get_guide, grep_guides, grouped_guides, guide_group, guide_sections, list_docs, list_guides, nav_manifest }
    cli.guide_store --> cli.mcp.resources.ResourceProvider._index_shared_guides { docs_dir, list_docs, list_guides }
    cli.jaccomplete --> cli.commands.tools.completions { static_shellcode as shellcode }
    cli.loader --> cli.dispatch.run_selected_command { load_handler }
    cli.manifest --> cli.commands.tools.completions { iter_command_meta }
    cli.manifest --> cli.dispatch.run_selected_command { get_command_meta }
    cli.manifest --> cli.loader.load_handler { get_command_meta }
    cli.manifest --> cli.manifest_help { GROUP_DISPLAY, GROUP_ORDER, TIER_ORDER, TIER_SECTIONS, iter_command_meta }
    cli.manifest --> cli.manifest_route.handle_manifest_route { TOMBSTONED_VERBS, known_command_names }
    cli.manifest --> cli.mcp_manifest.get_command { get_command_meta }
    cli.manifest --> cli.mcp_manifest.list_commands { get_groups, iter_command_meta }
    cli.manifest_help --> cli.manifest_route._render_version_line { _TITLE, _color, _use_color }
    cli.manifest_help --> cli.manifest_route.handle_manifest_route { format_curated_help, format_logo, format_verbose_help }
    cli.manifest_parse --> cli.dispatch.run_selected_command { build_command_parser }
    cli.manifest_route --> cli.cli.jac_version { resolve_cli_version }
    cli.manifest_route --> cli.cli.start_cli { handle_manifest_route }
    cli.manifest_route --> scale.injector.binary.deploy_generation_refusal { resolve_cli_version }
    cli.manifest_route --> scale.injector.binary.host_toolchain_path { resolve_cli_version }
    cli.manifest_route --> scale.observability.prometheus_metrics.PrometheusMetricsCollector.__post_init__ { resolve_cli_version }
    cli.manifest_route --> scale.tests.deploy.test_client_build_fail_fast { resolve_cli_version }
    cli.manifest_route --> scale.tests.deploy.test_memory_trigger_guard { resolve_cli_version }
    cli.manifest_route --> scale.tests.deploy.test_version_pin { resolve_cli_version }
    cli.manifest_route --> scale.tests.misc.test_metrics { resolve_cli_version }
    cli.mcp_manifest --> cli.mcp.tools.get_command { get_command as manifest_get_command }
    cli.mcp_manifest --> cli.mcp.tools.list_commands { list_commands as manifest_list_commands }
    cli.workpool --> cli.commands.analysis._check_retire { env_int, should_retire }
    cli.workpool --> cli.commands.analysis._check_rss_cap_mb { env_int }
    cli.workpool --> cli.commands.analysis._maybe_malloc_trim { maybe_malloc_trim }
    cli.workpool --> cli.commands.analysis.check { WorkPool, forced_serial, jobs_setting, pool_available, resolve_jobs }
    cli.workpool --> cli.commands.analysis.format { WorkPool, forced_serial, jobs_setting, pool_available, resolve_jobs }
    cli.workpool --> cli.commands.analysis.test { jobs_setting }
    cli.workpool --> dist.precompile_bytecode._precompile_retire { WORKER_MEM_BYTES, env_int, maybe_malloc_trim, should_retire, worker_rss_mb }
    cli.workpool --> dist.precompile_bytecode.precompile_native_unit { maybe_malloc_trim }
    cli.workpool --> dist.precompile_bytecode.precompile_unit_context { maybe_malloc_trim }
    cli.workpool --> dist.precompile_bytecode.run_precompile { WORKER_MEM_BYTES, WorkPool, env_int, forced_serial, jobs_setting, pool_available, resolve_jobs }
    cli.workpool --> testing.test_runner { WorkPool, should_retire as _should_retire, worker_rss_mb as _worker_rss_mb }
    cli.workpool --> testing.test_runner._test_retire { env_int }
    cli.workpool --> testing.test_runner.resolve_jobs { resolve_jobs as _resolve_pool_jobs }
    cli.console --> project.compiler_host.ProjectHost.note { console }
    cli.workpool --> dist.precompile_bytecode.prebuild_native_units { WorkPool }
    cli.workpool --> testing.test_runner._test_rss_cap_mb { env_int }
    cli.workpool --> dist.precompile_bytecode.seal_bootstrap { WORKER_MEM_BYTES, WorkPool, pool_available, resolve_jobs }
    cli.console --> packages.commands | packages.install | packages.publish | packages.verify { console }
    cli.command --> cli.commands.native { Arg, ArgKind, CommandSpec }
    cli.console --> cli.commands.native { console }
    cli.workpool --> cli.commands.analysis._settle_check_heap { maybe_malloc_trim, worker_rss_mb }
    cli.workpool --> server.server.JacAPIServer._validate_or_raise { cpu_quota }
    cli.workpool --> server.server.JacAPIServer.serve_background { cpu_quota }
    cli.workpool --> server.settings { cpu_quota, memory_headroom_bytes }
    cli.commands.analysis --> cli.commands.build.build { check }
    comptime cli.commands.analysis --> cli.manifest { SPEC_CHECK, SPEC_EXPLAIN, SPEC_FORMAT, SPEC_GEN_PARSER, SPEC_PRECOMMIT, SPEC_TEST }
    comptime cli.commands.architecture --> cli.manifest { SPEC_ARCH }
    comptime cli.commands.browse --> cli.manifest { SPEC_BROWSE }
    cli.commands.build --> cli.commands.execution._build_plan { build }
    comptime cli.commands.build --> cli.manifest { SPEC_BUILD }
    comptime cli.commands.cache --> cli.manifest { SPEC_CACHE }
    cli.commands.cli_helpers --> cli.commands.execution { proc_file as _proc_file }
    cli.commands.cli_helpers --> cli.commands.tools { proc_file as _proc_file }
    comptime cli.commands.code --> cli.manifest { SPEC_CODE }
    comptime cli.commands.config --> cli.manifest { SPEC_CONFIG }
    comptime cli.commands.db --> cli.manifest { SPEC_DB }
    cli.commands.execution --> cli.cli_boot._run_bundled_app { run_jab_image }
    comptime cli.commands.execution --> cli.manifest { SPEC_RUN, SPEC_X }
    cli.commands.execution --> client.targets.web_target.WebTarget.start { serve }
    cli.commands.execution --> scale.tests.server.test_serve { _find_free_port }
    comptime cli.commands.fix --> cli.manifest { SPEC_FIX }
    comptime cli.commands.guide --> cli.manifest { SPEC_GUIDE }
    comptime cli.commands.mcp --> cli.manifest { SPEC_MCP_CMD }
    cli.commands.native_build --> cli.commands.build._build_app { native_build }
    cli.commands.native_build --> cli.commands.build.build { native_build }
    cli.commands.native_build --> cli.commands.execution._build_plan { native_build }
    cli.commands.native_build --> dist.seal.bake_native_payloads { native_build }
    comptime cli.commands.precompile --> cli.manifest { SPEC_PRECOMPILE }
    cli.commands.project --> cli.commands.build._build_app { bundle }
    cli.commands.project --> cli.commands.execution.x { script }
    comptime cli.commands.project --> cli.manifest { SPEC_CLEAN, SPEC_CREATE, SPEC_INSTALL, SPEC_REMOVE, SPEC_UPDATE }
    comptime cli.commands.tools --> cli.manifest { SPEC_COMPLETIONS, SPEC_DOT, SPEC_LSP, SPEC_TOOL }
    cli.commands.analysis --> packages.publish.check_gate { check }
    comptime cli.commands.project --> cli.manifest { SPEC_PUBLISH }
    comptime cli.commands.native --> cli.manifest { SPEC_NATIVE }
    cli.mcp.compiler_bridge --> cli.mcp.tools.ToolProvider.call_tool { CompilerBridge }
    cli.mcp.compiler_bridge --> cli.mcp.tools.get_ast { CompilerBridge }
    cli.mcp.compiler_bridge --> cli.mcp.tools.graph_visualize { CompilerBridge }
    cli.mcp.compiler_bridge --> cli.mcp.tools.jac_to_js { CompilerBridge }
    cli.mcp.compiler_bridge --> cli.mcp.tools.jac_to_py { CompilerBridge }
    cli.mcp.compiler_bridge --> cli.mcp.tools.lint_jac { CompilerBridge }
    cli.mcp.compiler_bridge --> cli.mcp.tools.run_jac { CompilerBridge }
    cli.mcp.mode --> cli.commands.mcp.mcp_cmd { set_mcp_mode }
    cli.mcp.mode --> cli.mcp.prompts.PromptProvider.list_prompts { disabled_prompts_for_mode, get_mcp_mode }
    cli.mcp.mode --> cli.mcp.tools.ToolProvider.list_tools { disabled_tools_for_mode, get_mcp_mode }
    cli.mcp.prompts --> cli.commands.mcp._print_mcp_inventory { PromptProvider }
    cli.mcp.prompts --> cli.mcp.protocol { PromptProvider }
    cli.mcp.prompts --> cli.mcp.protocol.build_engine { PromptProvider }
    cli.mcp.protocol --> cli.mcp.server.JacMcpServer.start { build_engine, serve_sse, serve_stdio, serve_streamable_http }
    cli.mcp.resources --> cli.commands.mcp._print_mcp_inventory { ResourceProvider }
    cli.mcp.resources --> cli.mcp.prompts.load_resource_content { get_resource_provider }
    cli.mcp.resources --> cli.mcp.protocol { ResourceProvider }
    cli.mcp.resources --> cli.mcp.protocol.build_engine { get_resource_provider }
    cli.mcp.resources --> cli.mcp.tools.get_example { get_resource_provider }
    cli.mcp.resources --> cli.mcp.tools.get_resource { get_resource_provider }
    cli.mcp.resources --> cli.mcp.tools.list_examples { get_resource_provider }
    cli.mcp.resources --> cli.mcp.tools.search_docs { get_resource_provider }
    cli.mcp.resources --> cli.mcp.tools.understand_jac_and_jaseci { get_resource_provider }
    cli.mcp.server --> cli.commands.mcp.mcp_cmd { JacMcpServer }
    cli.mcp.tools --> cli.commands.mcp._print_mcp_inventory { ToolProvider }
    cli.mcp.tools --> cli.mcp.protocol { ToolProvider }
    cli.mcp.tools --> cli.mcp.protocol.build_engine { ToolProvider }
    cli.shadcn.cli --> cli.commands.project._create_body { stash_create_theme }
    cli.shadcn.cli --> cli.commands.project.install { run_shadcn_add }
    cli.shadcn.cli --> cli.commands.project.remove { run_shadcn_remove }
    comptime cli.shadcn.cli --> cli.manifest { SPEC_RETHEME }
    cli.shadcn.cli --> project.template_registry._register_builtin_shadcn_template { register_project_template }
    cli.shadcn.shadcn_handler --> cli.shadcn.cli.run_shadcn_add { add_shadcn_components }
    cli.shadcn.shadcn_handler --> cli.shadcn.cli.run_shadcn_remove { remove_shadcn_components }
    cli.shadcn.shadcn_handler --> cli.shadcn.theme_handler { _registry_dir, load_registry, resolve_single_component }
    cli.shadcn.theme_handler --> cli.shadcn.cli._shadcn_post_create { materialize_themed_starter, normalize_shadcn_config }
    cli.shadcn.theme_handler --> cli.shadcn.cli.retheme { retheme_project }
    client.artifact --> client.client_bundle { ClientBundle, ClientBundleError, prebuilt_bundle }
    client.artifact --> client.serving { client_output_dir }
    client.artifact --> server.server { ClientBundleError }
    client.artifact --> server.server.ModuleIntrospector.ensure_bundle { prebuilt_bundle }
    client.asset_processor --> client.jac_client_compiler { AssetProcessor }
    client.auth_contract --> client.client_react_core { SignupResult }
    client.auth_contract --> client.client_runtime { SignupResult }
    client.auth_contract --> client.client_runtime_core { SignupResult }
    client.auth_contract --> client.solid_runtime { SignupResult }
    client.cli --> cli.commands.build._build_app { run_client_build }
    client.cli --> cli.commands.execution.serve { run_client_start }
    client.cli --> cli.commands.project.install { run_npm_add }
    client.cli --> cli.commands.project.remove { run_npm_remove }
    comptime client.cli --> cli.manifest { SPEC_SETUP }
    client.client_bundle --> client.compiler { ClientBuildInputs, ClientBundle, ClientBundleError }
    client.client_bundle --> client.compiler.ViteCompiler._compile_wasm_module { client_program }
    client.client_bundle --> client.compiler.ViteCompiler.prepare_bundle { client_program }
    client.client_bundle --> client.import_processor { ClientBundleError }
    client.client_bundle --> client.jac_client_compiler { ClientBundleError }
    client.client_bundle --> client.npm_provider { ClientBundleError }
    client.client_bundle --> client.route_scanner { ClientBundleError }
    client.client_bundle --> client.vite_bundler { ClientBundleError }
    client.client_bundle --> client.vite_client_bundle { ClientBuildInputs, ClientBundle, ClientBundleBuilder, ClientBundleError }
    client.client_bundle --> client.vite_client_bundle.ViteClientBundleBuilder._emitted_digest { emitted_tree_digest }
    type client.client_bundle --> compiler.driver.build_services { ClientBundleBuilder }
    client.client_bundle --> compiler.driver.client_graph.collect_client_graph { ClientBundleError }
    client.client_bundle --> compiler.tests.test_client_codegen_facts { _client_target_module, _ensure_js_generated }
    client.client_bundle --> dist.source.client.write_client { client_program }
    type client.client_bundle --> runtime.build_services { ClientBundleBuilder }
    type client.client_bundle --> runtime.runtime { ClientBundle, ClientBundleBuilder }
    client.client_bundle --> server.hmr.HotReloader._recompile_client_unified { ClientBundleError }
    client.client_diagnostics --> client.cli.run_client_start { is_debug_mode }
    client.client_diagnostics --> server.endpoints.pages.register_diagnostics_endpoints.client_error { log_client_error }
    type client.client_diagnostics --> server.hmr { ClientDiagnostic }
    client.client_diagnostics --> server.hmr.HotReloader.record_client_event { classify_client_payload }
    client.client_diagnostics --> server.hmr.HotReloader.record_error { build_failure_diagnostic, diagnostics_from_alerts }
    client.client_diagnostics --> server.server.JacAPIServer._ensure_client_bundle { format_build_diagnostics }
    client.client_react_core --> client.client_runtime_native { __createJacSchema, __jacReportError, jacIsLoggedIn, useJacForm }
    client.client_runtime_core --> client.client_runtime { BridgeError as _BridgeError, BridgeRejected as _BridgeRejected, BridgeTimeout as _BridgeTimeout, BridgeUnavailable as _BridgeUnavailable, ErrorFallback as ___ErrorFallback, __bridgeApiBase as ___bridgeApiBase, __bridgeErrorFor as ___bridgeErrorFor, __bridgeErrorFromFetch as ___bridgeErrorFromFetch, __cacheGet as ___cacheGet, __cacheSet as ___cacheSet, __cachedEndpointCall as ___cachedEndpointCall, __createJacSchema as ___createJacSchema, __doFuncFetch as ___doFuncFetch, __doWalkerFetch as ___doWalkerFetch, __evictOldest as ___evictOldest, __getApiBaseUrl as ___getApiBaseUrl, __getCacheState as ___getCacheState, __getEndpointEffects as ___getEndpointEffects, __getLocalStorage as ___getLocalStorage, __invalidateEndpoint as ___invalidateEndpoint, __isFresh as ___isFresh, __jacCallFunction as ___jacCallFunction, __jacClearCache as ___jacClearCache, __jacDesktopBroker as ___jacDesktopBroker, __jacInstallErrorHandlers as ___jacInstallErrorHandlers, __jacPollBrokerSession as ___jacPollBrokerSession, __jacReactErrorHandler as ___jacReactErrorHandler, __jacReportError as ___jacReportError, __jacSleep as ___jacSleep, __jacSpawn as ___jacSpawn, __normalizeCredential as ___normalizeCredential, __normalizeIdentity as ___normalizeIdentity, __overlaps as ___overlaps, __removeLocalStorage as ___removeLocalStorage, __setLocalStorage as ___setLocalStorage, __unwrapFormSchema as ___unwrapFormSchema, errorOverlay as ___errorOverlay, jacIsLoggedIn as _jacIsLoggedIn, jacLogin as _jacLogin, jacLogout as _jacLogout, jacSetToken as _jacSetToken, jacSignup as _jacSignup, jacSpawn as _jacSpawn, jacSsoLogin as _jacSsoLogin, navigate as _navigate }
    client.client_runtime_core --> client.solid_runtime { BridgeError as _BridgeError, BridgeRejected as _BridgeRejected, BridgeTimeout as _BridgeTimeout, BridgeUnavailable as _BridgeUnavailable, ErrorFallback as ___ErrorFallback, __bridgeApiBase as ___bridgeApiBase, __bridgeErrorFor as ___bridgeErrorFor, __bridgeErrorFromFetch as ___bridgeErrorFromFetch, __cacheGet as ___cacheGet, __cacheSet as ___cacheSet, __cachedEndpointCall as ___cachedEndpointCall, __createJacSchema as ___createJacSchema, __doFuncFetch as ___doFuncFetch, __doWalkerFetch as ___doWalkerFetch, __evictOldest as ___evictOldest, __getApiBaseUrl as ___getApiBaseUrl, __getCacheState as ___getCacheState, __getEndpointEffects as ___getEndpointEffects, __getLocalStorage as ___getLocalStorage, __invalidateEndpoint as ___invalidateEndpoint, __isFresh as ___isFresh, __jacCallFunction as ___jacCallFunction, __jacClearCache as ___jacClearCache, __jacDesktopBroker as ___jacDesktopBroker, __jacInstallErrorHandlers as ___jacInstallErrorHandlers, __jacPollBrokerSession as ___jacPollBrokerSession, __jacReactErrorHandler as ___jacReactErrorHandler, __jacReportError as ___jacReportError, __jacSleep as ___jacSleep, __jacSpawn as ___jacSpawn, __normalizeCredential as ___normalizeCredential, __normalizeIdentity as ___normalizeIdentity, __overlaps as ___overlaps, __removeLocalStorage as ___removeLocalStorage, __setLocalStorage as ___setLocalStorage, __unwrapFormSchema as ___unwrapFormSchema, errorOverlay as ___errorOverlay, jacIsLoggedIn as _jacIsLoggedIn, jacLogin as _jacLogin, jacLogout as _jacLogout, jacSetToken as _jacSetToken, jacSignup as _jacSignup, jacSpawn as _jacSpawn, jacSsoLogin as _jacSsoLogin, navigate as _navigate }
    client.client_surface --> client.jac_to_js.JacToJSCompiler.add_runtime_imports { prepend_active_runtime_globals }
    client.client_surface --> compiler.backends.es.esast_gen_pass.EsastGenPass._inject_runtime_import { runtime_import_source }
    client.client_surface --> compiler.backends.es.esast_gen_pass.EsastGenPass._jsx_fragment { backend_jsx_factory_name }
    client.client_surface --> server.hmr.HotReloader._recompile_client_code { prepend_active_runtime_globals }
    client.client_surface --> testing.cl_test_runner._run_harness { prepend_active_runtime_globals }
    type client.compiler --> client.targets.client_dev_common { ViteCompiler }
    client.compiler --> client.vite_client_bundle { ViteCompiler }
    type client.compiler --> runtime.prepared { ViteCompiler }
    client.config_loader --> client.asset_processor.AssetProcessor.copy_custom_asset_types { JacClientConfig }
    client.config_loader --> client.client_deps { JacClientConfig }
    client.config_loader --> client.compiler.ViteCompiler._create_pages_entry_content { JacClientConfig }
    client.config_loader --> client.jac_client_compiler.JacClientCompiler.compile { JacClientConfig as PwaConfig }
    client.config_loader --> client.jac_client_compiler.JacClientCompiler.copy_root_assets { JacClientConfig }
    client.config_loader --> client.targets.mobile_target { JacClientConfig }
    client.config_loader --> client.targets.react_native.common { JacClientConfig }
    client.config_loader --> client.targets.web_target._pwa_enabled { JacClientConfig }
    client.config_loader --> client.vite_bundler { JacClientConfig }
    client.desktop_config --> client.targets.desktop.cef_shell.cef_build { get_desktop_config }
    client.desktop_config --> client.targets.desktop.desktop_target.DesktopTarget.build { get_desktop_config }
    client.desktop_config --> client.targets.desktop.desktop_target.DesktopTarget.engine { get_desktop_config }
    client.desktop_config --> client.targets.desktop.macos_bundle { DesktopIdentity }
    client.desktop_config --> client.targets.desktop.webview_shell._assemble_native_host { get_desktop_config }
    client.desktop_plugin_config --> client.desktop_config._validate_plugin_keys { _desktop_config_schema }
    client.desktop_plugin_config --> project.template_registry._register_builtin_client_templates { JacDesktopPluginConfig }
    client.endpoint_cache --> client.client_react_core { __cacheGet as cache___cacheGet, __cacheSet as cache___cacheSet, __cachedEndpointCall as cache___cachedEndpointCall, __endpointKey, __evictOldest as cache___evictOldest, __getCacheState as cache___getCacheState, __getEndpointEffects as cache___getEndpointEffects, __invalidateEndpoint as cache___invalidateEndpoint, __isFresh as cache___isFresh, __jacClearCache, __overlaps as cache___overlaps }
    client.endpoint_cache --> client.client_runtime_core { __cacheGet as cache___cacheGet, __cacheSet as cache___cacheSet, __cachedEndpointCall as cache___cachedEndpointCall, __endpointKey, __evictOldest as cache___evictOldest, __getCacheState as cache___getCacheState, __getEndpointEffects as cache___getEndpointEffects, __invalidateEffects as cache___invalidateEffects, __invalidateEndpoint as cache___invalidateEndpoint, __isFresh as cache___isFresh, __jacClearCache as cache___jacClearCache, __overlaps as cache___overlaps }
    client.import_processor --> client.jac_client_compiler { ImportProcessor }
    client.jac_client_compiler --> client.compiler { JacClientCompiler }
    client.jac_client_compiler --> client.targets.react_native.build { JacClientCompiler }
    client.jac_client_compiler --> compiler.tests.xbackend_equiv.run_js_module_fixture { JacClientCompiler }
    client.jac_to_js --> client.jac_client_compiler { JacToJSCompiler }
    client.npm_provider --> client.client_deps._default_client_deps { CORE_DEV_DEPS, CORE_RUNTIME_DEPS, OPTIONAL_RUNTIME_DEPS }
    client.npm_provider --> client.config_loader { CORE_DEV_DEPS, CORE_RUNTIME_DEPS, LEGACY_META_PACKAGES, OPTIONAL_RUNTIME_DEPS, app_npm_deps }
    client.npm_provider --> client.plugin_config.JacClientPluginConfig.register_ecosystem_providers { NpmProvider }
    client.npm_provider --> dist.publish.npm_builder._react_peer_floor { CORE_RUNTIME_DEPS }
    client.npm_provider --> dist.publish.runtime_npm._peer_versions { CORE_RUNTIME_DEPS, OPTIONAL_RUNTIME_DEPS }
    client.plugin_config --> client.desktop_plugin_config._load_desktop_template { _load_template }
    client.plugin_config --> project.providers.initialize_provider_registry { JacClientPluginConfig }
    client.plugin_config --> project.template_registry._register_builtin_client_templates { JacClientPluginConfig }
    client.preact_entry --> compiler.backends.es.backends.preact.PreactBackend.build_entry_script { build_simple_preact_entry_script }
    client.react_entry --> compiler.backends.es.backends.react.ReactBackend.build_entry_script { build_simple_react_entry_script }
    client.react_entry --> compiler.backends.es.backends.react.ReactBackend.build_pages_entry_script { build_pages_react_entry_script }
    client.route_scanner --> client.jac_client_compiler { RouteScanner, resolve_route_exports }
    client.route_scanner --> client.jac_client_compiler.JacClientCompiler._check_entry_renders_routes { entry_drops_route_children }
    client.route_scanner --> client.jac_client_compiler.JacClientCompiler._warn_pages_without_routes { describe_pages_without_routes }
    client.route_scanner --> client.jac_client_compiler.JacClientCompiler._warn_unrouted_pages { describe_unrouted_pages }
    client.route_scanner --> compiler.driver.application.prepare_route_metadata { RouteScanner }
    client.runtime_source --> client.compiler.ViteCompiler.compile_runtime_utils { resolve_client_runtime_cl_path }
    client.runtime_source --> client.vite_bundler.ViteBundler._generate_vite_config_content { JAC_VIRTUAL_MODULE_SOURCES }
    client.runtime_source --> dist.publish.runtime_npm._runtime_source_path { resolve_client_runtime_cl_path }
    client.runtime_source --> dist.publish.runtime_npm.build_runtime_tarball { resolve_client_runtime_cl_path }
    client.runtime_source --> dist.publish.runtime_npm.runtime_pkg_name { client_runtime_cl_basename }
    client.runtime_source --> project.modresolver._resolve_jac_virtual_module { jac_virtual_module_basenames, resolve_client_runtime_cl_path }
    client.serving --> client.targets.web_target._generate_index_html { HeaderBuilder }
    client.serving --> client.vite_bundler._dev_head_scripts { HeaderBuilder }
    client.serving --> runtime.runtime.JacServe.get_client_js { JacClient }
    client.serving --> runtime.runtime.JacServe.render_page { JacClient }
    client.solid_entry --> compiler.backends.es.backends.solid.SolidBackend.build_entry_script { build_simple_solid_entry_script }
    client.solid_entry --> compiler.backends.es.backends.solid.SolidBackend.build_pages_entry_script { build_pages_solid_entry_script }
    client.source_mapping --> client.client_diagnostics { JacLocator, SourceLocation, _npm_specifier }
    client.source_mapping --> client.jac_client_compiler.JacClientCompiler._write_source_map { generate_source_map_json }
    client.source_mapping --> scale.tests.server.test_build_status_endpoint._reset_client_globals { _error_rate_limiter, _locator_cache, _mapper_cache }
    client.source_mapping --> server.endpoints.pages.register_diagnostics_endpoints.client_error { _error_rate_limiter }
    client.source_mapping --> server.hmr.HotReloader.record_client_event { _error_rate_limiter }
    client.vite_bundler --> cli.commands.execution._start_vite_dev_server { ViteBundler }
    client.vite_bundler --> cli.commands.execution.serve._announce_ready { DEV_PROXY_PREFIXES }
    client.vite_bundler --> client.compiler { ViteBundler }
    client.vite_bundler --> client.npm_provider.regenerate_and_install { ViteBundler }
    type client.vite_bundler --> client.targets.client_dev_common { ViteBundler }
    client.vite_bundler --> client.targets.client_dev_common.dev_proxy_paths { DEV_PROXY_PREFIXES }
    client.vite_bundler --> client.targets.client_dev_common.prepare_vite_dev_compilation { ViteBundler }
    client.vite_bundler --> client.targets.desktop.desktop_target.DesktopTarget.build { API_BASE_URL_ENV_VAR }
    client.vite_bundler --> client.targets.static_target { ViteBundler }
    client.vite_bundler --> client.targets.web_target { ViteBundler }
    client.vite_bundler --> client.vite_client_bundle.make_client_bundle_builder { ViteBundler }
    client.vite_bundler --> dist.source.client.write_client { ViteBundler }
    client.vite_client_bundle --> client.targets.client_dev_common.prepare_vite_dev_compilation { make_client_bundle_builder }
    client.vite_client_bundle --> client.targets.mobile_target.MobileTarget._compile_native_jac_modules { ViteClientBundleBuilder }
    client.vite_client_bundle --> client.targets.web_target.WebTarget.build { make_client_bundle_builder }
    client.vite_client_bundle --> compiler.driver.application._prepare { make_client_bundle_builder }
    client.vite_client_bundle --> compiler.driver.build_services.CompilerBuildServices.client_builder { make_client_bundle_builder }
    client.vite_client_bundle --> compiler.driver.application._prepare_revision { make_client_bundle_builder }
    client.client_surface --> compiler.backends.es.esast_gen_pass { WASM_HOST_MODULE }
    client.config_loader --> compiler.driver.application._prepare_revision { JacClientConfig }
    client.js_engine --> client.js_runtime.js_runtime_path { node_executable }
    client.js_runtime --> cli.commands.execution._run_node_tool { js_runtime_path }
    client.js_runtime --> client.cli.run_npm_add_global { js_runtime_path, run_pm }
    client.js_runtime --> client.js_engine.node_executable { ensure_node_link }
    client.js_runtime --> client.npm_provider.regenerate_and_install { js_runtime_path }
    client.js_runtime --> client.targets.node_tooling_common { js_runtime_path, run_pm }
    client.js_runtime --> client.vite_bundler { js_runtime_path, run_pm }
    client.js_runtime --> dist.payload.assemble._bundle_bun { write_bun_record }
    client.js_runtime --> dist.payload.fetch { BUN_VERSION }
    client.js_runtime --> dist.payload.fetch.fetch_bun { _probe_bun, write_bun_record }
    client.js_runtime --> dist.seal.ensure_client_dist { js_runtime_path }
    client.js_runtime --> testing.cl_test_runner._run_harness { js_runtime_path }
    client.targets.build_common --> client.targets.client_dev_common { SUBPROCESS_TIMEOUT_SHORT }
    client.targets.build_common --> client.targets.react_native.build { artifact_mtime }
    client.targets.build_common --> client.targets.react_native.common { SUBPROCESS_TIMEOUT_BUILD_NATIVE }
    client.targets.client_dev_common --> client.targets.desktop.webview_shell.webview_dev { _ClientHmrHandler, ensure_watchdog_common, install_dev_signal_handlers, prepare_vite_dev_compilation, resolve_port_or_next_available, stop_dev_watcher, terminate_dev_processes }
    client.targets.client_dev_common --> client.targets.mobile_target { _ClientHmrHandler, ensure_watchdog_common, install_dev_signal_handlers, resolve_port_or_next_available, start_backend_server_common, stop_dev_watcher, terminate_dev_processes }
    client.targets.client_dev_common --> client.targets.react_native.dev { invalidate_runtime_module_cache, setup_android_port_reverse_common }
    client.targets.client_dev_common --> client.targets.web_target.WebTarget.dev { _ClientHmrHandler, dev_proxy_paths, ensure_watchdog_common, prepare_vite_dev_compilation, stop_dev_watcher, terminate_dev_processes }
    client.targets.mobile_target --> client.targets.register { MobileTarget }
    client.targets.node_tooling_common --> client.targets.react_native.common { resolve_node_tool as _node_resolve_node_tool, run_manifest_install as _node_run_manifest_install }
    client.targets.node_tooling_common --> client.vite_bundler._build_vite_command { resolve_node_tool_entry }
    client.targets.pwa_build --> client.targets.web_target.WebTarget.build { apply_pwa }
    client.targets.pwa_build --> client.targets.web_target.WebTarget.setup { ensure_pwa_icons }
    client.targets.register --> client.targets.registry.get_target_registry { register_targets }
    client.targets.registry --> client.cli { ClientTarget, target_for_app }
    client.targets.registry --> client.cli.run_client_build { target_for_kind }
    client.targets.registry --> client.cli.run_client_start { target_for_kind }
    client.targets.registry --> client.npm_provider.app_npm_deps { KIND_TARGET }
    client.targets.registry --> client.targets.mobile_target { ClientTarget }
    client.targets.registry --> client.targets.register { get_target_registry }
    client.targets.registry --> client.targets.web_target { ClientTarget }
    client.targets.static_target --> client.targets.register { StaticTarget }
    client.targets.web_target --> client.targets.desktop.desktop_target { WebTarget }
    client.targets.web_target --> client.targets.mobile_target.MobileTarget.build { WebTarget }
    client.targets.web_target --> client.targets.register { WebTarget }
    client.targets.web_target --> client.targets.static_target { WebTarget }
    client.targets.web_target --> dist.seal.ensure_client_dist { WebTarget }
    client.targets.desktop._dev_launch --> client.targets.desktop.cef_shell { desktop_app_runtime_env, ensure_dev_build_env }
    client.targets.desktop._dev_launch --> client.targets.desktop.desktop_build { desktop_launch_env }
    client.targets.desktop._dev_launch --> client.targets.desktop.webview_shell { desktop_app_runtime_env, ensure_dev_build_env, jac_desktop_deps_shell_export, jac_desktop_webkit_shell_export }
    client.targets.desktop._host_bootstrap --> client.targets.desktop.cef_shell { _fused_runtime_import_block, _host_boot_py }
    client.targets.desktop._host_bootstrap --> client.targets.desktop.webview_shell { _generate_host_source }
    client.targets.desktop.app_layout --> client.targets.desktop.macos_bundle { AppLayout }
    client.targets.desktop.app_layout --> client.targets.desktop.native.host_boot { AppLayout }
    client.targets.desktop.app_layout --> client.targets.desktop.webview_shell { AppLayout }
    client.targets.desktop.cef_shell --> client.targets.desktop.desktop_target.DesktopTarget.build { cef_build }
    client.targets.desktop.cef_shell --> client.targets.desktop.desktop_target.DesktopTarget.dev { cef_dev_unsupported }
    client.targets.desktop.cef_shell --> client.targets.desktop.desktop_target.DesktopTarget.start { cef_start }
    client.targets.desktop.desktop_build --> client.targets.desktop.cef_shell { _bundle_runtime, _find_cef_dir, _jac_bin, _jac_subprocess_env, _patch_host_rpath, _stage_fused_runtime, build_cef_dispatch, build_cef_subprocess, stage_program }
    client.targets.desktop.desktop_build --> client.targets.desktop.native.cef.build { build_cef_dispatch, build_cef_subprocess }
    client.targets.desktop.desktop_build --> client.targets.desktop.webview_shell { _bundle_runtime, _find_webview_dir, _jac_bin, _jac_subprocess_env, _stage_fused_runtime, stage_program }
    client.targets.desktop.desktop_build --> toolchains.manager.setup_toolchain { _find_cef_dir, _find_webview_dir }
    client.targets.desktop.desktop_target --> client.targets.register { DesktopTarget }
    client.targets.desktop.macos_bundle --> client.targets.desktop.webview_shell { write_bundle_metadata }
    client.targets.desktop.webview_shell --> client.targets.desktop.desktop_target.DesktopTarget.build { webview_build }
    client.targets.desktop.webview_shell --> client.targets.desktop.desktop_target.DesktopTarget.dev { webview_dev }
    client.targets.desktop.webview_shell --> client.targets.desktop.desktop_target.DesktopTarget.start { webview_start }
    client.targets.desktop.native.broker_extension --> client.targets.desktop.native.host_boot.serve_program { DesktopBrokerExtension }
    client.targets.desktop.native.oauth_broker --> client.targets.desktop.native.broker_extension { CLOSE_PAGE, DEFAULT_PREFIX, LOOPBACK_HOSTS, PendingAuth, SAME_SITE_VALUES, SessionStore, build_sso_login_url }
    client.targets.desktop.native.oauth_broker --> client.targets.desktop.native.host_boot.boot { SessionStore }
    client.targets.desktop.native.cef.cef --> client.targets.desktop.native.cef.cef_smoke { cef_cleanup, new_cef_browser }
    client.targets.desktop.native.cef.cef --> client.targets.desktop.native.cef.cef_test_host { cef_cleanup, cef_execute_subprocess, cef_open_browser, cef_run_loop, cef_startup }
    include client.targets.desktop.native.cef.cef_platform --> client.targets.desktop.native.cef.cef_dispatch;
    include client.targets.desktop.native.cef.cef_platform --> client.targets.desktop.native.cef.cef_subprocess;
    client.targets.desktop.native.webview.webview --> client.targets.desktop.native.plugin_bridge { Webview, respond }
    client.targets.react_native.build --> client.targets.mobile_target { entry_module_for, lint_native_incompatible_usage, lint_unmapped_tags, read_user_js_sources, run_eas_local_build, run_eas_update_opt_in, run_expo_prebuild, run_gradle_assemble, run_xcodebuild_ios, stage_compiled_entry, stage_native_image_assets, strip_css_imports, write_native_entry }
    client.targets.react_native.build --> client.targets.react_native.dev { lint_native_incompatible_usage, lint_unmapped_tags, read_user_js_sources, stage_compiled_entry, stage_native_image_assets, strip_css_imports, write_api_base_shim, write_native_entry }
    client.targets.react_native.build --> client.targets.react_native.scaffold { build_native_index_entry_body }
    client.targets.react_native.common --> client.targets.mobile_target { DEFAULT_APP_ID, DEFAULT_APP_NAME, DEFAULT_APP_SLUG, detect_lan_ipv4, resolve_rn_project_dir }
    client.targets.react_native.common --> client.targets.mobile_target.MobileTarget.start { normalize_rn_platform }
    client.targets.react_native.common --> client.targets.react_native.build { SUBPROCESS_TIMEOUT_BUILD, resolve_node_tool }
    client.targets.react_native.common --> client.targets.react_native.dev { resolve_node_tool }
    client.targets.react_native.common --> client.targets.react_native.scaffold { DEFAULT_APP_ID, DEFAULT_APP_NAME, DEFAULT_APP_SLUG, EAS_CLI_VERSION, EXPO_SDK_VERSION, REACT_NATIVE_VERSION, run_manifest_install }
    client.targets.react_native.config --> client.targets.mobile_target { _resolve_rn_android_builder, _resolve_rn_eas_profile, _resolve_rn_eas_update_branch, _resolve_rn_eas_update_enabled, _resolve_rn_eas_update_message, _resolve_rn_ios_builder, _resolve_rn_release }
    client.targets.react_native.dev --> client.cli.run_client_start { JAC_RN_DEV_HOST_ENV }
    client.targets.react_native.dev --> client.targets.mobile_target { JAC_RN_DEV_HOST_ENV, inject_dev_api_base_url, resolve_metro_port, restore_app_json, rn_hmr_on_jac_changed, run_expo_start, setup_android_port_reverse }
    client.targets.react_native.html_tag_map --> client.client_runtime_native { RN_HTML_TEXT_TAGS as _TEXT_TAGS, RN_HTML_VIEW_TAGS as _VIEW_TAGS }
    client.targets.react_native.html_tag_map --> client.targets.react_native.build { supported_rn_html_tags }
    client.targets.react_native.html_tag_map --> compiler.passes.jsx_intrinsic_guard_pass._suggestion_for { rn_tag_suggestions }
    client.targets.react_native.scaffold --> client.targets.mobile_target { ensure_native_deps_installed, write_expo_scaffold }
    compiler.boundary_audit --> client.compiler.ViteCompiler.prepare_bundle { boundary_audit }
    compiler.c_interop --> compiler.backends.native.na_ir_gen_pass { c_builtin_kind, c_type_arg, foreign_read_copies, foreign_struct_of_type, is_builtin_pin_call, is_pinned_type, is_ptr_type, is_ptr_view_type }
    compiler.c_interop --> compiler.backends.py.jcir_gen_pass.JcirGenPass._c_copy_rewrite { foreign_read_copies }
    compiler.c_interop --> compiler.backends.py.jcir_gen_pass.JcirGenPass._c_interop_call_rewrite { c_type_spec, is_builtin_pin_call }
    compiler.c_interop --> compiler.backends.py.jcir_gen_pass.JcirGenPass._clib_block_desc { c_type_spec, is_foreign_struct_archetype, is_opaque_c_archetype }
    compiler.c_interop --> compiler.passes.ownership_check_pass { c_call_borrows_args, is_c_value_type, is_ptr_view_type, reads_foreign_storage }
    compiler.c_interop --> compiler.passes.rc_facts_pass.result_ownership { foreign_read_copies }
    compiler.c_interop --> compiler.passes.type_checker_pass.TypeCheckPass._c_arg_instance { c_type_arg }
    compiler.c_interop --> compiler.passes.type_checker_pass.TypeCheckPass._c_plain_data { foreign_struct_of_type, is_ptr_type }
    compiler.c_interop --> compiler.passes.type_checker_pass.TypeCheckPass._check_c_interop_call { c_type_arg, is_builtin_pin_call, is_ptr_type, opaque_c_of_type }
    compiler.c_interop --> compiler.passes.type_checker_pass.TypeCheckPass._check_c_interop_import { c_type_arg, foreign_struct_of_type, is_foreign_struct_archetype, is_pinned_type }
    compiler.c_interop --> compiler.passes.type_checker_pass.TypeCheckPass._check_c_type_use { clib_import_of }
    compiler.c_interop --> compiler.passes.type_checker_pass.TypeCheckPass._foreign_struct_contains { foreign_struct_of_type }
    compiler.c_interop --> compiler.passes.type_checker_pass.TypeCheckPass._opaque_member { opaque_c_of_type }
    compiler.c_interop --> compiler.types.type_evaluator.TypeEvaluator._assign_c_interop_args { c_type_arg }
    compiler.c_interop --> compiler.types.type_evaluator.TypeEvaluator._is_typed_c_declaration { c_builtin_kind }
    compiler.expr_keys --> compiler.backends.native.na_ir_gen_pass { type_tag_borrows }
    compiler.expr_keys --> compiler.passes.cfg_build_pass.CFGBuildPass._wire_bool_operands { collect_narrowing_symbols }
    compiler.expr_keys --> compiler.passes.cfg_build_pass.CFGBuildPass._wire_compr_filters { collect_narrowing_symbols }
    compiler.expr_keys --> compiler.passes.cfg_build_pass.CFGBuildPass.cfg_collect_affected { collect_assigned_symbols }
    compiler.expr_keys --> compiler.passes.cfg_build_pass.CFGBuildPass.enter_assert_stmt { collect_narrowing_symbols }
    compiler.expr_keys --> compiler.passes.cfg_build_pass.CFGBuildPass.enter_else_if { collect_narrowing_symbols }
    compiler.expr_keys --> compiler.passes.cfg_build_pass.CFGBuildPass.enter_if_stmt { collect_narrowing_symbols }
    compiler.expr_keys --> compiler.passes.cfg_build_pass.CFGBuildPass.exit_if_else_expr { collect_narrowing_symbols }
    compiler.expr_keys --> compiler.passes.ownership_check_pass { type_tag_borrows }
    compiler.expr_keys --> compiler.symbol_utils { classify_condition_key, collect_assigned_symbols, collect_assignment_target_keys, collect_narrowing_symbols, find_destructure_index_path, get_expr_key, int_subscript_suffix, reference_key_deps }
    compiler.expr_keys --> compiler.types.ownership { type_tag_borrows }
    compiler.field_semantics --> compiler.backends.es.esast_gen_pass.EsastGenPass._field_constructor_args { positional_field_names }
    compiler.field_semantics --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_archetype { positional_field_names }
    compiler.field_semantics --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_call { field_initialization, is_field_marker }
    compiler.field_semantics --> compiler.backends.py.jcir_gen_pass.JcirGenPass.exit_has_var { is_field_marker }
    compiler.field_semantics --> compiler.passes.type_checker_pass.TypeCheckPass.exit_has_var { field_initialization }
    compiler.field_semantics --> compiler.types.type_evaluator.TypeEvaluator._build_field_params { field_initialization }
    compiler.intrinsic_registry --> compiler.backends.native.na_ir_gen_pass { IntrinsicEntry }
    compiler.intrinsic_registry --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_call { INTRINSIC_REGISTRY }
    compiler.intrinsic_registry --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_intrinsic { IntrinsicDispatch }
    compiler.intrinsic_registry --> compiler.passes.type_checker_pass.TypeCheckPass._check_intrinsic_collision { IntrinsicRegistry }
    compiler.intrinsic_registry --> compiler.symbol_utils.classify_call { IntrinsicRegistry }
    compiler.intrinsic_registry --> compiler.symbol_utils.intrinsic_registry_if_ready { INTRINSIC_REGISTRY }
    compiler.intrinsic_registry --> compiler.types.type_evaluator.TypeEvaluator._intrinsic_function_type { IntrinsicRegistry }
    compiler.jc_materialize --> compiler.jc_unit { hint_commentdata, hint_srcdiag, jc_mz_obj, jc_mz_run }
    compiler.native_scope --> compiler.backends.native.kernel_resolve.kernel_plan { kernel_root_path }
    compiler.native_scope --> compiler.driver.selfhost.SelfHostCache.resolve { in_native_scope_path }
    compiler.native_scope --> compiler.frontend.codeinfo._inferred_native_path { scope_allows_inferred_path }
    compiler.native_scope --> compiler.frontend.codeinfo.resolve_native_module { in_native_scope_path }
    compiler.native_scope --> compiler.placement.placement_facts.native_unit { in_native_scope_path }
    compiler.native_scope --> compiler.placement.placement_solver._native_deps_ok { in_native_scope_path }
    compiler.native_scope --> dist.precompile_bytecode.seal_native { kernel_root_path }
    compiler.passes --> compiler.tools.code_intel { Alert }
    compiler.symbol_utils --> compiler.backends.es.esast_gen_pass { return_type_is_jsx }
    compiler.symbol_utils --> compiler.backends.es.esast_gen_pass.EsastGenPass._bind_client_value_refs { client_bridged_endpoint, client_value_ref_targets, element_display_name }
    compiler.symbol_utils --> compiler.backends.es.esast_gen_pass.EsastGenPass._build_spawn_arg_object { collect_field_names, symbol_owner_archetype }
    compiler.symbol_utils --> compiler.backends.es.esast_gen_pass.EsastGenPass._build_spawn_runtime_call { symbol_owner_archetype }
    compiler.symbol_utils --> compiler.backends.es.esast_gen_pass.EsastGenPass._partition_client_import_items { ClientImportVerdict, classify_client_import_item, is_client_boundary_import, report_dead_client_import }
    compiler.symbol_utils --> compiler.backends.es.esast_gen_pass.EsastGenPass._resolve_call_ability { ability_of_symbol }
    compiler.symbol_utils --> compiler.backends.es.esast_gen_pass.EsastGenPass._resolve_source_module { resolve_import_source_module }
    compiler.symbol_utils --> compiler.backends.es.esast_gen_pass.EsastGenPass.exit_module { report_client_bare_import_uses }
    compiler.symbol_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._callee_ability_of { resolved_callee }
    compiler.symbol_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_method_call_inner { imported_module_name }
    compiler.symbol_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_synthetic_call { ability_of_symbol, classify_call, resolve_expr_symbol }
    compiler.symbol_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._isinstance_type_name { CallKind, classify_call }
    compiler.symbol_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._native_module_call_target { imported_module_name }
    compiler.symbol_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._unregistered_class_target { resolve_expr_symbol }
    compiler.symbol_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._visit_nonprimary_ancestor_methods { collect_method_names }
    compiler.symbol_utils --> compiler.backends.py.jcir_gen_pass.JcirGenPass._exit_func_call_impl { CallKind, classify_call }
    compiler.symbol_utils --> compiler.passes.ownership_check_pass { CallKind, classify_call }
    compiler.symbol_utils --> compiler.passes.ownership_check_pass.OwnershipCheckPass._callee_ability { resolved_callee }
    compiler.symbol_utils --> compiler.passes.static_analysis_pass.StaticAnalysisPass._check_client_imports { ClientImportVerdict, classify_client_import_item, is_client_boundary_import, report_dead_client_import, resolve_import_source_module }
    compiler.symbol_utils --> compiler.passes.static_analysis_pass.StaticAnalysisPass._check_placement_warnings { report_placement_warnings, report_serverless_kind_errors }
    compiler.symbol_utils --> compiler.passes.type_checker_pass { return_type_is_jsx }
    compiler.symbol_utils --> compiler.passes.type_checker_pass.TypeCheckPass._check_intrinsic_collision { intrinsic_registry_if_ready }
    compiler.symbol_utils --> compiler.passes.type_checker_pass.TypeCheckPass.exit_func_call { ability_of_symbol, classify_call, resolve_expr_symbol }
    compiler.symbol_utils --> compiler.placement.placement_solver.PlacementApplyPass._run_impl { report_serverless_kind_errors }
    compiler.symbol_utils --> compiler.placement.placement_solver._pull_boundary_import { symbol_linked_source_module }
    compiler.symbol_utils --> compiler.types.type_evaluator.TypeEvaluator._get_type_from_flow_node { collect_assignment_target_keys, find_destructure_index_path }
    compiler.symbol_utils --> compiler.types.type_evaluator.TypeEvaluator._get_type_of_lhs_assignment { find_destructure_index_path }
    compiler.symbol_utils --> compiler.types.type_evaluator.TypeEvaluator._intrinsic_function_type { intrinsic_registry_if_ready }
    compiler.symbol_utils --> compiler.types.type_evaluator.TypeEvaluator._is_sv_async_call { ClientImportVerdict, classify_client_import_item, resolve_import_source_module }
    compiler.symbol_utils --> compiler.types.type_evaluator.TypeEvaluator._loop_body_writes_target { collect_assignment_target_keys }
    compiler.symbol_utils --> compiler.types.type_evaluator.TypeEvaluator._resolve_importer_path { resolve_importer_path_from_node }
    compiler.symbol_utils --> compiler.types.type_evaluator.TypeEvaluator.create_key_for_reference { int_subscript_suffix }
    compiler.symbol_utils --> compiler.types.type_evaluator.TypeEvaluator.flow_pred_never_returns { resolve_expr_symbol }
    compiler.type_registry --> compiler.backends.es.esast_gen_pass.EsastGenPass._audit_free_identifiers { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.es.esast_gen_pass.EsastGenPass._ensure_emitters { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.es.esast_gen_pass.EsastGenPass._primitive_type_ref { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.es.esast_gen_pass.EsastGenPass.exit_archetype { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.es.esast_gen_pass.EsastGenPass.exit_func_call { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.es.esast_gen_pass.EsastGenPass.exit_raise_stmt { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.es.esast_gen_pass.EsastGenPass.exit_try_stmt { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.es.esast_gen_pass._raised_exc_identity { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.es.jac_runtime_js._build_exc_runtime_js { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.es.jac_runtime_js._build_types_runtime_js { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.native.foreign { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.native.na_ir_gen_pass { JacTypeEntry }
    compiler.type_registry --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass.__post_init__ { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._c_scalar_llvm { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_name { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_sized_builtin_call { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._ensure_emitters { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._get_exc_descendants { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._get_or_register_exc_type { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.c_interop._spec_for_name { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.c_interop.c_type_spec { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.passes.layout_pass { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.passes.mtir_gen_pass { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.passes.ownership_check_pass { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.passes.ownership_check_pass.OwnershipCheckPass._handled_by_enclosing_try { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.passes.type_checker_pass.TypeCheckPass._c_plain_data { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.passes.type_checker_pass.TypeCheckPass._stamp_fixed_width { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.passes.type_checker_pass.TypeCheckPass.exit_archetype { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.passes.type_checker_pass.TypeCheckPass.exit_type_alias { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.passes.wasm_contract._host_type { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.passes.wasm_contract.value_contract { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.symbol_utils.classify_call { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.types.fixed_width { JAC_TYPE_REGISTRY, NumericKind }
    compiler.type_registry --> compiler.types.operations.is_int_kind_type { JAC_TYPE_REGISTRY, NumericKind }
    compiler.type_registry --> compiler.types.type_evaluator.TypeEvaluator._assign_class { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.types.type_evaluator.TypeEvaluator._brand_distinct_alias { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.types.type_evaluator.TypeEvaluator._extern_field_type { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.types.type_evaluator.TypeEvaluator._extern_scalar_type { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.types.type_evaluator.TypeEvaluator._is_typed_c_declaration { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.types.type_utils.primitive_type_name_of { JAC_TYPE_REGISTRY }
    compiler.erased_imports --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_call { contextmanager_ability, erased_identity_call_arg }
    compiler.erased_imports --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._ctxmgr_callee { contextmanager_ability }
    compiler.erased_imports --> compiler.field_semantics.is_field_marker { erased_import_binds }
    compiler.erased_imports --> compiler.passes.capability_check_pass.native_capability_violations { contextmanager_ability, is_contextmanager_decorator }
    compiler.field_semantics --> compiler.backends.native.na_ir_gen_pass { field_initialization }
    type compiler.intrinsic_registry --> compiler.symbol_utils { IntrinsicRegistry }
    compiler.jc_materialize --> compiler.jc_unit { jc_mz_shape_keys }
    compiler.kernel_target --> compiler.backends.native.kernel_stage0 { KERNEL_TARGET_FORMAT, KernelTarget, read_kernel_target, set_kernel_target }
    compiler.kernel_target --> compiler.driver.jir.sidecar_unit_paths | compiler.driver.native_iface | compiler.native_scope.scope_module_path { target_pkg_root }
    compiler.kernel_target --> compiler.driver.jir.get_module_cache_path { is_target_package_path, kernel_target_active }
    compiler.kernel_target --> compiler.frontend.codeinfo { active_kernel_target, is_target_package_path, kernel_target_active, kernel_target_generation, target_pkg_root }
    compiler.kernel_target --> compiler.native_scope.kernel_root_module | compiler.placement.placement_facts.native_lowered { active_kernel_target }
    compiler.kernel_target --> compiler.native_scope.scope_modules | compiler.placement.placement_facts.native_only { active_kernel_target }
    compiler.kernel_target --> compiler.native_scope.native_scope_path_suffixes { kernel_target_generation }
    compiler.kernel_target --> compiler.placement.placement_facts._toolchain_rel { target_package_rel }
    type compiler.kernel_target --> compiler.backends.native.kernel_resolve { KernelTarget }
    compiler.native_compiler as _jc --> project.compiler_host.ProjectHost.native_parse;
    compiler.native_compiler --> project.kernel_check.analysis_kernel { ensure_loaded }
    compiler.native_scope --> compiler.backends.native.kernel_stage0.running_kernel_target { KERNEL_ROOT_MODULE, NATIVE_SCOPE }
    compiler.native_scope --> compiler.driver.program.JacProgram.declared_codespace { package_host_edge }
    compiler.native_scope --> compiler.driver.program.JacProgram.infers_native_codespace { in_native_scope_path, package_host_edge }
    compiler.native_scope --> dist.precompile_bytecode.native_roots { kernel_root_path }
    compiler.symbol_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._copy_call_kind { imported_module_name }
    compiler.symbol_utils --> compiler.placement.placement_export.collect_placement_rows { ClientImportVerdict, classify_client_import_item, is_client_boundary_import, resolve_import_source_module }
    compiler.kernel_target --> compiler.driver.jir._ct_pkg_ref { target_package_rel }
    compiler.kernel_target --> compiler.driver.jir._ct_row_path { target_pkg_root }
    compiler.native_scope --> dist.precompile_bytecode._compiler_kernel_units { kernel_root_path, native_scope_paths }
    compiler.native_scope --> compiler.driver.wiring.is_kernel_abi_contract { KERNEL_ABI_CONTRACT_REL }
    compiler.c_interop --> compiler.passes.ownership_check_pass { is_ptr_type }
    compiler.kernel_target --> compiler.driver.jir.native_producer_digest { target_pkg_root }
    compiler.erased_imports --> compiler.passes.rc_facts_pass.result_ownership { erased_identity_call_arg }
    compiler.jc_ask --> compiler.frontend.kernel_host.KernelHost.ask { ask_host }
    compiler.jc_ask --> compiler.jc_unit { set_host_callback, take_host_answer }
    compiler.native_compiler --> project.kernel_compile.kernel_route { ensure_loaded }
    type compiler.native_compiler --> project.kernel_snapshot { NativeCompiler }
    compiler.native_compiler --> project.kernel_snapshot.loaded_kernel { ensure_loaded }
    compiler.native_scope --> dist.precompile_bytecode.seal_native { in_native_scope_path }
    compiler.boundary_rules --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._export_mixed_native { ability_crossing }
    compiler.boundary_rules --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass.finish { archetype_refusals, signature_crossings, signature_refusals }
    compiler.boundary_rules --> compiler.passes.placement_pass.NativeLegality.settle { ability_crossing }
    compiler.boundary_rules --> compiler.passes.placement_pass.bridged_use_crosses { ability_crossing }
    compiler.boundary_rules --> compiler.passes.placement_pass.uncrossable_native { ability_crossing }
    compiler.c_interop --> compiler.backends.native.na_ir_gen_pass { c_array_elem, c_bytes_array_values, c_bytes_elem_shape, c_bytes_literal, c_scalar_constant, c_string_literal, c_variadic_param, clib_block_defines, clib_global_of_name, clib_import_of, foreign_field_of, is_builtin_addressof_call, is_va_list_type, named_function_of }
    compiler.c_interop --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_unary { c_lent_arg_elem }
    compiler.c_interop --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._ensure_clib_struct { foreign_struct_of_type }
    compiler.c_interop --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._final_scalar_value { c_scalar_constant, final_glob_value }
    compiler.c_interop --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._final_variant_value { final_glob_value }
    compiler.c_interop --> compiler.backends.py.jcir_gen_pass { c_variadic_param }
    compiler.c_interop --> compiler.backends.py.jcir_gen_pass.JcirGenPass._c_interop_call_rewrite { c_lent_arg_elem, c_lent_param, c_param_type, c_variadic_param, is_ptr_type, named_function_of }
    compiler.c_interop --> compiler.backends.py.jcir_gen_pass.JcirGenPass._c_vararg_rewrite { c_type_spec }
    compiler.c_interop --> compiler.backends.py.jcir_gen_pass.JcirGenPass._is_c_global_value { clib_global_of_name, is_builtin_addressof_call }
    compiler.c_interop --> compiler.passes.layout_pass.open_dispatch { is_clib_archetype }
    compiler.c_interop --> compiler.passes.ownership_check_pass { clib_import_of }
    compiler.c_interop --> compiler.passes.type_checker_pass.TypeCheckPass._borrowed_scalar_param { clib_import_of, is_ptr_type }
    compiler.c_interop --> compiler.passes.type_checker_pass.TypeCheckPass._c_const_problem { c_array_elem, c_bytes_elem_shape, c_bytes_literal, c_scalar_constant, c_string_literal, foreign_struct_of_type, is_builtin_addressof_call, is_ptr_type, named_function_of }
    compiler.c_interop --> compiler.passes.type_checker_pass.TypeCheckPass._check_c_function_def { c_variadic_param, foreign_struct_of_type }
    compiler.c_interop --> compiler.passes.type_checker_pass.TypeCheckPass._check_c_global_decl { c_array_elem }
    compiler.c_interop --> compiler.passes.type_checker_pass.TypeCheckPass._check_c_global_use { clib_global_of_name, foreign_struct_of_type, is_builtin_addressof_call }
    compiler.c_interop --> compiler.passes.type_checker_pass.TypeCheckPass._check_c_interop_call { c_string_literal, clib_global_of_name, is_builtin_addressof_call }
    compiler.c_interop --> compiler.passes.type_checker_pass.TypeCheckPass._check_c_variadic_args { c_variadic_param }
    compiler.c_interop --> compiler.passes.type_checker_pass.TypeCheckPass._check_c_variadic_def { c_variadic_param }
    compiler.c_interop --> compiler.passes.type_checker_pass.TypeCheckPass.exit_assignment { c_bytes_array_definition }
    compiler.c_interop --> compiler.types.type_evaluator { is_va_list_type }
    compiler.c_interop --> compiler.types.type_evaluator.TypeEvaluator._c_lent_args { c_abi_callee, c_lent_elem }
    compiler.capability_notes --> compiler.boundary_rules { TARGET_NATIVE, TARGET_SERVER }
    type compiler.capability_notes --> compiler.driver.progstate { CapabilityNote }
    compiler.capability_notes --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._export_mixed_native { TARGET_NATIVE, TARGET_SERVER }
    compiler.capability_notes --> compiler.passes.placement_pass.NativeLegality.settle { TARGET_NATIVE, TARGET_SERVER }
    compiler.capability_notes --> compiler.passes.placement_pass.PlacementPass._run_undecided { capability_notes_of }
    compiler.capability_notes --> compiler.passes.placement_pass.bridged_use_crosses { TARGET_NATIVE, TARGET_SERVER }
    compiler.capability_notes --> compiler.passes.placement_pass.build_native_legality { TARGET_NATIVE, capability_notes_of }
    compiler.capability_notes --> compiler.passes.placement_pass.element_requirements { TARGET_NATIVE, capability_notes_of }
    compiler.capability_notes --> compiler.passes.placement_pass.uncrossable_native { TARGET_NATIVE, TARGET_SERVER }
    compiler.capability_notes --> compiler.passes.static_analysis_pass.StaticAnalysisPass._check_undefined_names { TARGET_NATIVE, note_capability, placement_neutral }
    compiler.capability_notes --> compiler.types.type_evaluator.TypeEvaluator.neutral_site { placement_neutral }
    compiler.capability_notes --> compiler.types.type_evaluator.TypeEvaluator.note_native { TARGET_NATIVE, note_capability }
    compiler.expr_keys --> compiler.passes.rc_facts_pass.method_returns_borrow { type_tag_borrows }
    compiler.kernel_target --> compiler.native_scope.binds_bare_arch_names { target_package_rel }
    compiler.native_bindings --> compiler.passes.layout_pass.record_interface_twins { interface_type, typeshed_stub_path }
    compiler.native_bindings --> compiler.passes.placement_pass.PlacementPass._check_conformance { conformance_mismatches, native_library_module_name, typeshed_stub_path, variant_mismatches }
    compiler.native_bindings --> compiler.passes.placement_pass.build_native_legality { binding_gaps, import_gaps }
    compiler.native_compiler --> compiler.backends.native.kernel_resolve.refuse_unloadable { load_failure }
    compiler.native_scope --> compiler.driver.jir.abi_contract_digest { KERNEL_ABI_CONTRACT_REL }
    compiler.native_scope --> compiler.frontend.codeinfo.native_arch_scope { binds_bare_arch_names }
    compiler.native_scope --> compiler.placement.placement_solver.native_closure_blocker { in_native_scope_path }
    compiler.native_scope --> compiler.placement.placement_solver.native_placement_candidate { in_native_scope_path }
    compiler.symbol_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_plain_trailer { imported_module_name }
    compiler.symbol_utils --> compiler.c_interop.c_abi_callee { resolved_callee }
    compiler.symbol_utils --> compiler.passes.placement_pass.PlacementPass._run_decided { report_serverless_kind_errors }
    compiler.symbol_utils --> compiler.passes.placement_pass.PlacementPass._run_undecided { report_serverless_kind_errors }
    compiler.symbol_utils --> compiler.types.type_evaluator.TypeEvaluator._narrowed_type_for_expr { reference_key_deps }
    compiler.type_registry --> compiler.backends.native.host_facts.primitive_methods_fact { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.backends.native.na_ir_gen_pass._caught_exception_class_name { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.c_interop.c_bytes_elem_shape { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.c_interop.c_scalar_constant { JAC_TYPE_REGISTRY }
    compiler.type_registry --> compiler.passes.type_checker_pass.TypeCheckPass._borrowed_scalar_param { JAC_TYPE_REGISTRY }
    compiler.backends.es --> compiler.backends.es.client_kernel_cache._lower { estree as es }
    compiler.backends.es --> compiler.tests.xbackend_equiv { EsastGenPass }
    compiler.backends.es --> compiler.tools.lang_tools { EsastGenPass, es_node_to_dict }
    compiler.backends.common.primitives --> compiler.backends.es.primitives_es { BuiltinEmitter, BytesEmitter, ComplexEmitter, DictEmitter, FloatEmitter, FrozensetEmitter, IntEmitter, ListEmitter, RangeEmitter, SetEmitter, StrEmitter, TupleEmitter }
    compiler.backends.common.primitives --> compiler.backends.native.primitives_native { BuiltinEmitter, BytesEmitter, ComplexEmitter, DictEmitter, FloatEmitter, FrozensetEmitter, IntEmitter, ListEmitter, RangeEmitter, SetEmitter, StrEmitter, TupleEmitter }
    compiler.backends.common.primitives --> compiler.backends.es.esast_gen_pass { PrimitiveEmitter }
    compiler.backends.common.primitives --> compiler.backends.es.jac_runtime_js._build_types_runtime_js { PrimitiveEmitter }
    compiler.backends.common.primitives --> compiler.backends.es.primitives_es { PrimitiveEmitter }
    compiler.backends.common.primitives --> compiler.backends.native.na_ir_gen_pass { PrimitiveEmitter }
    compiler.backends.es.es_unparse --> compiler.backends.es.client_kernel_cache._lower { es_to_js }
    compiler.backends.es.es_unparse --> compiler.backends.es.esast_gen_pass { JSCodeGenerator, es_to_js }
    compiler.backends.es.es_unparse --> compiler.backends.es.esast_gen_pass.EsastGenPass._try_primitive_op { JSCodeGenerator }
    compiler.backends.es.es_unparse --> compiler.backends.es.esast_gen_pass.EsastGenPass.exit_func_call { JSCodeGenerator }
    compiler.backends.es.es_unparse --> compiler.backends.es.jac_runtime_js._build_types_runtime_js { JSCodeGenerator }
    compiler.backends.es.es_unparse --> compiler.tests.xbackend_equiv { es_to_js }
    compiler.backends.es.es_unparse --> compiler.tools.lang_tools { es_to_js }
    compiler.backends.es.esast_gen_pass --> compiler.backends.es.client_kernel_cache._lower { EsastGenPass }
    type compiler.backends.es.esast_gen_pass --> compiler.backends.es.jsx_processor { EsastGenPass }
    compiler.backends.es.esast_gen_pass --> compiler.tests.test_client_codegen_facts { EsastGenPass }
    compiler.backends.es.esast_gen_pass --> dist.publish.npm_sources._compile_module { EsastGenPass }
    compiler.backends.es.estree as es --> compiler.backends.es.backends.react;
    compiler.backends.es.estree as es --> compiler.backends.es.backends.solid;
    compiler.backends.es.estree as es --> compiler.backends.es.esast_gen_pass;
    compiler.backends.es.estree as es --> compiler.backends.es.framework_backend;
    compiler.backends.es.estree as es --> compiler.backends.es.free_ident_audit;
    type compiler.backends.es.estree --> compiler.backends.es.jsx_processor { Expression }
    compiler.backends.es.estree as es --> compiler.backends.es.reactive_intent;
    compiler.backends.es.estree as es --> compiler.backends.es.view_ir;
    type compiler.backends.es.estree --> compiler.frontend.codeinfo { IndexInfo, Node as EsNode, SliceInfo }
    compiler.backends.es.estree --> compiler.tests.xbackend_equiv { Node as EsNode }
    compiler.backends.es.estree --> compiler.tools.lang_tools { Node as EsNode }
    type compiler.backends.es.framework_backend --> client.client_surface { FrameworkBackend }
    compiler.backends.es.framework_backend --> compiler.backends.es.backends.react { FrameworkBackend }
    compiler.backends.es.framework_backend --> compiler.backends.es.backends.registry { FrameworkBackend }
    compiler.backends.es.framework_backend --> compiler.backends.es.backends.solid { FrameworkBackend }
    compiler.backends.es.framework_backend --> compiler.backends.es.esast_gen_pass { FrameworkBackend }
    compiler.backends.es.free_ident_audit --> compiler.backends.es.esast_gen_pass { FreeIdentifier, RUNTIME_PRELUDE_GLOBALS, client_ambient_globals, free_identifiers }
    compiler.backends.es.jac_runtime_js --> client.jac_client_compiler.JacClientCompiler.emit_prelude { write_jac_prelude_file }
    compiler.backends.es.jac_runtime_js --> client.vite_bundler.ViteBundler._generate_vite_config_content { JAC_PRELUDE_BASENAME }
    compiler.backends.es.jac_runtime_js --> compiler.backends.es.client_kernel_cache._lower { JAC_PRELUDE_MODULE }
    compiler.backends.es.jac_runtime_js --> compiler.backends.es.esast_gen_pass.EsastGenPass._inject_runtime_import { JAC_PRELUDE_MODULE }
    compiler.backends.es.jac_runtime_js --> compiler.backends.es.esast_gen_pass.EsastGenPass.exit_module { JAC_PRELUDE_MODULE, build_osp_core_js, build_osp_driver_js }
    compiler.backends.es.jac_runtime_js --> compiler.tests.xbackend_equiv._prelude_cwd { stage_jac_prelude_package }
    compiler.backends.es.jac_runtime_js --> compiler.tests.xbackend_equiv.run_js_module_fixture { stage_jac_prelude_package }
    compiler.backends.es.jac_runtime_js --> dist.publish.runtime_npm._point_at_packaged_prelude { JAC_PRELUDE_BASENAME, JAC_PRELUDE_MODULE }
    compiler.backends.es.jac_runtime_js --> dist.publish.runtime_npm.build_runtime_tarball { JAC_PRELUDE_BASENAME, build_jac_prelude_module }
    compiler.backends.es.jac_runtime_js --> testing.cl_test_runner._point_at_staged_prelude { point_jac_prelude_at }
    compiler.backends.es.jac_runtime_js --> testing.cl_test_runner._run_harness { JAC_PRELUDE_BASENAME, build_jac_prelude_module }
    compiler.backends.es.jsx_processor --> compiler.backends.es.esast_gen_pass { EsJsxProcessor }
    compiler.backends.es.primitives_es --> compiler.backends.es.esast_gen_pass { ESBuiltinEmitter, ESEmitCtx }
    compiler.backends.es.primitives_es --> compiler.backends.es.jac_runtime_js._build_types_runtime_js { ESBuiltinEmitter, ESEmitCtx }
    compiler.backends.es.reactive_intent --> compiler.backends.es.backends.react { AsyncBoundary, Effect, RefField, StateField, StateUpdate }
    compiler.backends.es.reactive_intent --> compiler.backends.es.backends.solid { AsyncBoundary, Effect, RefField, StateField, StateUpdate }
    compiler.backends.es.reactive_intent --> compiler.backends.es.esast_gen_pass { AsyncBoundary, Effect, RefField, StateField, StateUpdate }
    compiler.backends.es.reactive_intent --> compiler.backends.es.framework_backend { AsyncBoundary, Effect, RefField, StateField, StateUpdate }
    compiler.backends.es.scoped_styles --> compiler.backends.es.esast_gen_pass { ScopedStyleSheet, load_style_annex }
    type compiler.backends.es.view_ir --> compiler.backends.es.backends.react { ViewElement }
    compiler.backends.es.view_ir --> compiler.backends.es.backends.react.ReactBackend.lower_view { ComponentTag, DynamicChild, DynamicTag, EachChild, ElementChild, HostTag, IfChild, SpreadAttr, TextChild }
    type compiler.backends.es.view_ir --> compiler.backends.es.backends.solid { ViewChild, ViewElement }
    compiler.backends.es.view_ir --> compiler.backends.es.backends.solid.SolidBackend._jsx_child_nodes { DynamicChild, EachChild, ElementChild, FragmentTag, IfChild, TextChild }
    compiler.backends.es.view_ir --> compiler.backends.es.backends.solid.SolidBackend._view_children_as_expr { ElementChild, FragmentTag }
    compiler.backends.es.view_ir --> compiler.backends.es.backends.solid.SolidBackend.lower_async_boundary { ComponentTag, DynamicAttr, DynamicChild, ElementChild, ViewElement }
    compiler.backends.es.view_ir --> compiler.backends.es.backends.solid.SolidBackend.lower_view { ComponentTag, FragmentTag, HostTag }
    compiler.backends.es.view_ir --> compiler.backends.es.backends.solid.SolidBackend.view_runtime_symbols { EachChild, ElementChild, IfChild }
    type compiler.backends.es.view_ir --> compiler.backends.es.framework_backend { ViewElement }
    type compiler.backends.es.view_ir --> compiler.backends.es.jsx_processor { DynamicAttr, EachChild, EventAttr, IfChild, RefAttr, SpreadAttr, StaticAttr, ViewChild, ViewElement }
    compiler.backends.es.view_ir --> compiler.backends.es.jsx_processor.EsJsxProcessor._lift_each { EachChild, ElementChild, ViewElement }
    compiler.backends.es.view_ir --> compiler.backends.es.jsx_processor.EsJsxProcessor._lift_if { IfChild }
    compiler.backends.es.view_ir --> compiler.backends.es.jsx_processor.EsJsxProcessor._split_key { DynamicAttr, StaticAttr }
    compiler.backends.es.view_ir --> compiler.backends.es.jsx_processor.EsJsxProcessor._view_arm { ElementChild }
    compiler.backends.es.view_ir --> compiler.backends.es.jsx_processor.EsJsxProcessor.element { ComponentTag, DynamicChild, DynamicTag, ElementChild, FragmentTag, HostTag, SlotChild, SpreadAttr, TextChild, ViewElement }
    compiler.backends.es.view_ir --> compiler.backends.es.jsx_processor.EsJsxProcessor.normal_attribute { DynamicAttr, EventAttr, RefAttr, StaticAttr }
    compiler.backends.es.js_paths --> compiler.backends.es.esast_gen_pass { convert_to_js_import_path, relative_js_specifier }
    compiler.backends.es.js_paths --> project.modresolver.resolve_module { convert_to_js_import_path }
    compiler.backends.es.client_kernel_cache --> project.compiler_host.ProjectHost.client_osp_core_js { osp_core_js }
    compiler.backends.es.es_unparse --> compiler.driver.unit_products.client_artifact_of { es_to_js_with_map }
    compiler.backends.es.estree as es --> compiler.backends.es.es_unparse;
    compiler.backends.es.estree as es --> compiler.backends.es.jsx_processor;
    compiler.backends.es.estree --> compiler.driver.unit_products.client_artifact_of { Node as EsNode }
    compiler.backends.es.free_ident_audit --> client.client_surface.with_runtime_globals { js_identifiers, js_top_level_declarations }
    compiler.backends.es.free_ident_audit --> compiler.backends.es.esast_gen_pass { js_identifiers }
    compiler.backends.es.primitives_es --> compiler.backends.es.esast_gen_pass { es_sized_cast }
    compiler.backends.es.primitives_es --> compiler.backends.es.esast_gen_pass.EsastGenPass._ensure_emitters { es_primitive_emitter }
    compiler.backends.es.primitives_es --> compiler.backends.es.jac_runtime_js._build_types_runtime_js { es_sized_cast }
    compiler.backends.es.view_ir --> compiler.backends.es.backends.react { DynamicAttr, EventAttr, RefAttr, StaticAttr, ViewLocator, view_attr_node }
    type compiler.backends.es.view_ir --> compiler.backends.es.backends.react { DynamicAttr, EventAttr, RefAttr, StaticAttr, ViewLocator }
    compiler.backends.es.view_ir --> compiler.backends.es.backends.solid { DynamicAttr, EachChild, EventAttr, IfChild, RefAttr, SpreadAttr, StaticAttr, ViewLocator }
    type compiler.backends.es.view_ir --> compiler.backends.es.backends.solid { DynamicAttr, EachChild, EventAttr, IfChild, RefAttr, SpreadAttr, StaticAttr, ViewLocator }
    type compiler.backends.es.view_ir --> compiler.backends.es.framework_backend { ViewLocator }
    compiler.backends.es.view_ir --> compiler.backends.es.jsx_processor.EsJsxProcessor.element { ViewLocator }
    compiler.backends.es.esast_gen_pass --> compiler.driver.pipeline.client_passes { EsastGenPass }
    compiler.backends.es.esast_gen_pass --> compiler.driver.pipeline.codegen_passes { EsastGenPass }
    compiler.backends.es.backends.preact --> compiler.backends.es.backends.registry.resolve_framework_backend { PreactBackend }
    compiler.backends.es.backends.react --> compiler.backends.es.backends.preact { ReactBackend }
    compiler.backends.es.backends.react --> compiler.backends.es.backends.registry.resolve_framework_backend { ReactBackend }
    compiler.backends.es.backends.react --> compiler.backends.es.esast_gen_pass.EsastGenPass._ensure_backend { ReactBackend }
    compiler.backends.es.backends.registry --> client.client_surface.prepend_active_runtime_globals { resolve_active_backend }
    compiler.backends.es.backends.registry --> client.compiler.ViteCompiler._create_pages_entry_content { resolve_active_backend }
    compiler.backends.es.backends.registry --> client.compiler.ViteCompiler.create_entry_file { resolve_active_backend }
    compiler.backends.es.backends.registry --> client.vite_bundler.ViteBundler._generate_vite_config_content { resolve_active_backend }
    compiler.backends.es.backends.registry --> compiler.driver.build_services.CompilerBuildServices.client_runtime_basename { resolve_active_backend, resolve_framework_backend }
    compiler.backends.es.backends.registry --> compiler.driver.compiler.JacCompiler._get_client_artifact { resolve_active_backend }
    compiler.backends.es.backends.solid --> compiler.backends.es.backends.registry.resolve_framework_backend { SolidBackend }
    compiler.backends.es.backends.registry --> compiler.backends.es.esast_gen_pass.EsastGenPass._ensure_backend { active_framework, resolve_framework_backend }
    compiler.backends.es.backends.registry --> compiler.driver.compiler.cached_client_pulls { resolve_active_backend }
    compiler.backends.es.backends.registry --> compiler.driver.unit_products.client_artifact_of { resolve_active_backend }
    compiler.backends.native.abi --> compiler.backends.native.na_ir_gen_pass { classify_foreign_fn }
    compiler.backends.native.abi --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._build_jc_layout { struct_layouts }
    compiler.backends.native.c_emit --> dist.native_product.write_native_product { emit_c }
    compiler.backends.native.c_emit --> dist.source.client.write_client { emit_c }
    compiler.backends.native.elf_linker --> compiler.backends.native.link_plan.link_artifact { ElfLinker }
    compiler.backends.native.foreign --> compiler.backends.native.abi.classify_foreign_fn { foreign_struct_layout }
    compiler.backends.native.foreign --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._clib_struct_layout { foreign_struct_layout }
    compiler.backends.native.foreign --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_call { declared_type_name }
    compiler.backends.native.foreign --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._foreign_fns { collect_foreign_fns }
    compiler.backends.native.foreign --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._foreign_model { collect_foreign_structs }
    compiler.backends.native.kernel_resolve --> compiler.native_compiler.ensure_loaded { resolve_kernel }
    compiler.backends.native.kernel_resolve --> dist.precompile_bytecode.seal_native { kernel_lib_name }
    compiler.backends.native.link_glue --> compiler.backends.native.link_plan { ENTRY_SYMBOL, GlueSpec, GlueUnit, REGION_DIED_HOOK, SHARED_INIT_SYMBOL, STR_NEW_SYMBOL, init_object_codegen, link_glue_ir }
    compiler.backends.native.link_glue --> compiler.backends.native.link_plan.callback_glue_ir { bind_shared_callbacks }
    compiler.backends.native.link_glue --> compiler.backends.native.link_plan.heap_glue_ir { inject_heap_accounting }
    compiler.backends.native.link_plan --> cli.commands.native_build { LinkPlan }
    compiler.backends.native.link_plan --> cli.commands.native_build.native_build { ArtifactKind, LinkPlanError, build_link_plan, link_artifact }
    compiler.backends.native.link_plan --> compiler.backends.native.kernel_resolve.kernel_plan { build_link_plan }
    compiler.backends.native.link_plan --> compiler.backends.native.na_compile_pass.NativeCompilePass._run_impl { SymbolCollision, jit_engine_for_module }
    compiler.backends.native.link_plan --> compiler.driver.compiler.JacCompiler._load_native_from_cache { jit_engine_for_cached }
    compiler.backends.native.link_plan --> compiler.driver.nativecache.NativeUnitRegistry.compile_unit { build_link_plan }
    compiler.backends.native.link_plan --> compiler.driver.pipeline_runner.wasm_ir { build_link_plan, wasm_program_ir }
    compiler.backends.native.link_plan --> dist.native_product.write_native_product { ArtifactKind, build_link_plan, link_artifact, optimize_merged_program, whole_program_module }
    compiler.backends.native.link_plan --> dist.precompile_bytecode.seal_native { ArtifactKind, build_link_plan, link_artifact }
    compiler.backends.native.linker_common --> compiler.backends.native.elf_linker { _align, _append_to_blob, _build_strtab, _find_entry_vaddr, _resolve_patch_site, _resolve_seg_vaddr }
    compiler.backends.native.linker_common --> compiler.backends.native.macho_linker { _align, _append_to_blob, _build_strtab, _find_entry_vaddr, _resolve_patch_site, _resolve_seg_vaddr, encode_uleb128 }
    compiler.backends.native.linker_common --> compiler.backends.native.pe_linker { _align, _append_to_blob, _resolve_seg_vaddr }
    compiler.backends.native.linker_common --> compiler.backends.native.static_link { object_undefined_symbols, select_ar_members }
    compiler.backends.native.linker_common --> compiler.backends.native.wasm_artifact.wasm_import_map { read_leb_name, read_uleb128 }
    compiler.backends.native.linker_common --> compiler.backends.native.wasm_build.wasm_import_map { read_leb_name, read_uleb128 }
    compiler.backends.native.linker_common --> compiler.backends.native.wasm_linker { encode_sleb128, encode_uleb128, encode_uleb128_padded5, read_leb_name, read_sleb128, read_uleb128 }
    compiler.backends.native.lowering --> compiler.backends.native.entry_points.validate_native_application { native_lowering_issues }
    compiler.backends.native.lowering --> compiler.backends.native.na_compile_pass.native_demoted_ir_symbols { NativeLoweringKind, native_lowering_issues }
    compiler.backends.native.lowering --> compiler.backends.native.na_compile_pass.require_native_ir { native_lowering_issues }
    compiler.backends.native.lowering --> compiler.backends.native.na_ir_gen_pass { NativeLoweringIssue, NativeLoweringKind }
    compiler.backends.native.lowering --> compiler.tests.test_prim_equivalence { native_lowering_issues }
    compiler.backends.native.macho_linker --> compiler.backends.native.link_plan.link_artifact { MachOLinker }
    compiler.backends.native.na_compile_pass --> cli.commands.analysis.explain { native_linked_ir_text }
    compiler.backends.native.na_compile_pass --> compiler.backends.native.entry_points.validate_native_application { native_demoted_ir_symbols, native_linked_ir_text }
    compiler.backends.native.na_compile_pass --> compiler.backends.native.link_plan { NATIVE_CODE_MODEL, NATIVE_RELOC_MODEL, optimize_unit }
    compiler.backends.native.na_compile_pass --> compiler.backends.native.wasm_build.prepare_wasm_module { optimize_unit }
    compiler.backends.native.na_compile_pass --> compiler.driver.nativecache.NativeUnitRegistry.object_for { emit_unit_object }
    compiler.backends.native.na_constants --> compiler.backends.native.na_ir_gen_pass { CLASS_DISPLAY_OFF, LIVE_NODE_NEXT_OFF, LIVE_NODE_RC_OFF, LIVE_NODE_SIZE, LIVE_NODE_TAG_OFF, LIVE_NODE_USER_OFF, NATIVE_OSPATH_FUNCS, NATIVE_OS_FUNCS, NATIVE_RANDOM_FUNCS, NATIVE_STRUCT_FUNCS, RC_BUFFERED_BIT, RC_COLOR_BLACK, RC_COLOR_GRAY, RC_COLOR_PURPLE, RC_COLOR_SHIFT, RC_COLOR_WHITE, RC_CYCLE_THRESHOLD }
    type compiler.backends.native.na_ir_gen_pass --> compiler.backends.native.primitives_native { NaIRGenPass }
    compiler.backends.native.pe_linker --> compiler.backends.native.link_plan.link_artifact { PeLinker }
    compiler.backends.native.primitives_native --> compiler.backends.native.na_ir_gen_pass { NativeDictEmitter, NativeEmitCtx, NativeSetEmitter }
    compiler.backends.native.primitives_native as _pn --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._ensure_emitters;
    compiler.backends.native.region_abi --> compiler.backends.native.na_ir_gen_pass { REGION_KERNEL_ABI }
    compiler.backends.native.static_link --> compiler.backends.native.link_plan { clib_needed_libs, clib_symbol_lib_map, collect_floor_archives, load_musl_static }
    compiler.backends.native.wasm_artifact --> client.compiler.ViteCompiler._compile_wasm_module { wasm_assets }
    compiler.backends.native.wasm_artifact --> dist.source.build.build_native_product { wasm_assets }
    compiler.backends.native.wasm_build --> cli.commands.native_build.native_build { app_declared_imports }
    compiler.backends.native.wasm_build --> compiler.backends.native.link_plan.link_wasm { emit_wasm_from_ir }
    compiler.backends.native.wasm_build --> compiler.driver.pipeline_runner.wasm_artifact { emit_wasm_from_ir }
    compiler.backends.native.wasm_build --> compiler.driver.pipeline_runner.wasm_ir { _assert_ir_rc_free, _project_gc_settings, app_declared_imports }
    compiler.backends.native.wasm_build --> dist.native_product.write_native_product { _assert_ir_rc_free }
    compiler.backends.native.wasm_build --> dist.source.client.write_client { prepare_wasm_module }
    compiler.backends.native.wasm_host_abi --> compiler.backends.native.wasm_artifact { WASM_HOST_MODULE }
    compiler.backends.native.wasm_host_abi --> compiler.backends.native.wasm_build._link_wasm_libc { WASM_HOST_ABI }
    compiler.backends.native.wasm_host_abi --> compiler.backends.native.wasm_build.emit_wasm_from_ir { WASM_HOST_ABI, WASM_HOST_MODULE }
    compiler.backends.native.wasm_host_abi --> dist.source.build.build_native_product { WASM_HOST_ABI, WASM_HOST_MODULE }
    compiler.backends.native.wasm_linker --> compiler.backends.native.wasm_build.emit_wasm_from_ir { WasmLinker }
    compiler.backends.native.wasm_linker --> dist.source.build.build_native_product { WasmLinker }
    compiler.backends.native.kernel_resolve --> compiler.backends.native.kernel_stage0 { KERNEL_DEV_LINK_MODE, kernel_plan }
    compiler.backends.native.kernel_resolve --> dist.precompile_bytecode.seal_native { SEALED_LINK_MODE }
    compiler.backends.native.kernel_stage0 --> compiler.backends.native.kernel_resolve.build_kernel { link_kernel }
    compiler.backends.native.link_plan --> compiler.backends.native.kernel_stage0.link_kernel { ArtifactKind, link_artifact }
    compiler.backends.native.link_plan --> dist.precompile_bytecode.prebuild_native_closure { build_link_plan }
    type compiler.backends.native.link_plan --> compiler.backends.native.kernel_resolve { LinkPlan }
    type compiler.backends.native.link_plan --> compiler.backends.native.kernel_stage0 { LinkResult }
    compiler.backends.native.linker_common --> compiler.backends.native.link_plan.link_artifact { object_undefined_symbols }
    compiler.backends.native.na_compile_pass --> compiler.driver.nativecache.NativeBuildSession.lower { settle_unit_ir }
    compiler.backends.native.na_constants --> compiler.backends.native.na_ir_gen_pass { JACVAL_ELLIPSIS_TAG, NATIVE_CONTAINER_CODES, NATIVE_COPY_FUNCS }
    compiler.backends.native.static_link --> compiler.backends.native.link_plan { load_outline_atomics }
    compiler.backends.native.na_constants --> compiler.backends.native.na_ir_gen_pass { EXC_LINEAGE_BITS, EXC_LINEAGE_MIX, EXC_LINEAGE_SLOTS }
    compiler.backends.native.na_compile_pass --> compiler.driver.nativecache.NativeUnitRegistry.emit_objects { emit_unit_objects }
    compiler.backends.native.na_constants --> compiler.backends.native.na_ir_gen_pass { RC_CYCLE_PACE, RC_UNTRACED_BIT }
    compiler.backends.native.link_glue --> compiler.backends.native.link_plan { RC_THREADED_SYMBOL }
    compiler.backends.native.na_compile_pass --> compiler.driver.nativecache.NativeBuildSession._optimize_in_parallel { optimize_unit_texts, require_native_ir }
    compiler.backends.native.floors --> dist.payload.vendor { WASM_FLOOR_MANIFEST }
    compiler.backends.native.host_facts --> project.compiler_host.ProjectHost.native_fact { host_native_fact }
    compiler.backends.native.kernel_resolve --> project.kernel_check.kernel_check { refuse_unloadable }
    compiler.backends.native.kernel_resolve --> project.kernel_compile.kernel_route { refuse_unloadable }
    compiler.backends.native.link_glue --> compiler.backends.native.link_plan { SHARED_MAIN_SYMBOL }
    type compiler.backends.native.link_plan --> compiler.backends.native.kernel_resolve { LinkResult }
    compiler.backends.native.linker_common --> compiler.backends.native.static_link { ArMember }
    compiler.backends.native.na_compile_pass --> compiler.driver.nativecache.NativeUnitRegistry.adopt_lowered { emit_unit_object, optimize_unit_texts, require_native_ir }
    compiler.backends.native.na_compile_pass --> compiler.driver.pipeline.native_object_passes { NativeCompilePass }
    compiler.backends.native.na_constants --> compiler.backends.native.abi.struct_layouts { FACT_SEP, FACT_STRUCT_LAYOUTS }
    compiler.backends.native.na_constants --> compiler.backends.native.host_facts { FACT_CODEC_NAME, FACT_CODEC_TABLES, FACT_IMPORT_PATHS, FACT_OS, FACT_PRIMITIVE_METHODS, FACT_SEALED_RUNTIME, FACT_SEP, FACT_STRUCT_LAYOUTS, FACT_TARGET }
    compiler.backends.native.na_constants --> compiler.backends.native.na_ir_gen_pass { CLASS_RECORD_ANCESTRY, CLASS_RECORD_STATICS, CLASS_RECORD_STATICS_COUNT, FACT_CODEC_NAME, FACT_CODEC_TABLES, FACT_OS, FACT_PRIMITIVE_METHODS, FACT_SEALED_RUNTIME, FACT_SEP, FACT_STRUCT_LAYOUTS, FACT_TARGET, UNBOUND_CAUGHT, VTABLE_SET_BUCKETS, VTABLE_SET_SYMBOL, stdlib_intercepted }
    compiler.backends.native.na_constants --> compiler.driver.native_iface.resolve_native_unit_ref { FACT_IMPORT_PATHS, FACT_SEP }
    compiler.backends.native.na_ir_gen_pass --> compiler.driver.pipeline.codegen_passes { NaIRGenPass }
    compiler.backends.native.na_ir_gen_pass --> compiler.driver.pipeline.native_ir_passes { NaIRGenPass }
    compiler.backends.native.na_ir_gen_pass --> compiler.driver.pipeline.native_lower_passes { NaIRGenPass }
    compiler.backends.native.primitives_native as emitters --> compiler.backends.native.host_facts.primitive_methods_fact;
    compiler.backends.native.primitives_native as _pm_pn --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._dispatch_primitive_method;
    compiler.backends.native.primitives_native as _pn --> compiler.backends.native.na_ir_gen_pass._native_emitter_of;
    compiler.backends.native.win_floor --> compiler.backends.native.link_glue.link_glue_ir { win_floor_ir }
    compiler.backends.native.win_floor --> compiler.backends.native.link_plan.link_artifact { WIN_CRT_DLL }
    compiler.backends.native.win_floor --> compiler.backends.native.pe_linker { win_import_dll, win_import_name }
    compiler.backends.native.win_floor_ir --> compiler.backends.native.win_floor.win_floor_ir { WIN_FLOOR_IR }
    compiler.backends.native.win_floor_ir --> compiler.backends.native.win_floor.win_import_dll { WIN_FLOOR_KERNEL32 }
    compiler.backends.native.llvm.binding as llvm --> cli.commands.execution._jab_native_bin;
    compiler.backends.native.llvm.binding as llvm --> cli.commands.native_build._application_ir;
    compiler.backends.native.llvm.binding as llvm --> compiler.backends.native.link_glue.bind_shared_callbacks;
    compiler.backends.native.llvm.binding as llvm --> compiler.backends.native.link_glue.init_object_codegen;
    compiler.backends.native.llvm.binding as llvm --> compiler.backends.native.link_plan;
    type compiler.backends.native.llvm.binding --> compiler.backends.native.link_plan { ExecutionEngine, ModuleRef, TargetMachine }
    compiler.backends.native.llvm.binding --> compiler.backends.native.llvm.binding.config { ffi }
    compiler.backends.native.llvm.binding --> compiler.backends.native.llvm.binding.context { ffi }
    compiler.backends.native.llvm.binding --> compiler.backends.native.llvm.binding.dylib { ffi }
    compiler.backends.native.llvm.binding --> compiler.backends.native.llvm.binding.executionengine { ffi, object_file, targets }
    compiler.backends.native.llvm.binding --> compiler.backends.native.llvm.binding.initfini { ffi }
    compiler.backends.native.llvm.binding --> compiler.backends.native.llvm.binding.linker { ffi }
    compiler.backends.native.llvm.binding --> compiler.backends.native.llvm.binding.module { ffi }
    compiler.backends.native.llvm.binding --> compiler.backends.native.llvm.binding.newpassmanagers { ffi }
    compiler.backends.native.llvm.binding --> compiler.backends.native.llvm.binding.object_file { ffi }
    compiler.backends.native.llvm.binding --> compiler.backends.native.llvm.binding.options { ffi }
    compiler.backends.native.llvm.binding --> compiler.backends.native.llvm.binding.targets { ffi }
    compiler.backends.native.llvm.binding --> compiler.backends.native.llvm.binding.value { ffi }
    compiler.backends.native.llvm.binding as llvm --> compiler.backends.native.na_compile_pass;
    type compiler.backends.native.llvm.binding --> compiler.backends.native.na_compile_pass { ModuleRef, TargetMachine }
    type compiler.backends.native.llvm.binding --> compiler.backends.native.wasm_build { ModuleRef, TargetMachine, ValueRef }
    compiler.backends.native.llvm.binding as llvm --> compiler.backends.native.wasm_build._load_libc_module;
    compiler.backends.native.llvm.binding as llvm --> compiler.backends.native.wasm_build.prepare_wasm_module;
    compiler.backends.native.llvm.binding as llvm --> compiler.driver.compiler.JacCompiler._load_native_from_cache;
    type compiler.backends.native.llvm.binding --> compiler.driver.compiler.JacCompiler._load_native_from_cache { ExecutionEngine }
    type compiler.backends.native.llvm.binding --> compiler.frontend.codeinfo { ExecutionEngine }
    compiler.backends.native.llvm.binding as llvm --> dist.seal.bake_native_payloads;
    type compiler.backends.native.llvm.ir --> compiler.frontend.codeinfo { Module as IRModule }
    compiler.backends.native.llvm.binding --> project.compiler_host.ProjectHost.default_target_triple { get_default_triple }
    compiler.backends.native.llvm.binding as llvm --> compiler.backends.native.host_facts.struct_layouts_fact;
    compiler.backends.native.llvm.binding as llvm --> compiler.backends.native.host_facts.target_fact;
    compiler.backends.native.llvm.ir as ir --> compiler.backends.native.abi;
    compiler.backends.native.llvm.ir as ir --> compiler.backends.native.lowering;
    compiler.backends.native.llvm.ir as ir --> compiler.backends.native.na_ir_gen_pass;
    compiler.backends.native.llvm.ir as ir --> compiler.backends.native.primitives_native;
    compiler.backends.native.llvm.shim_path --> compiler.backends.native.llvm.binding.ffi { shim_path }
    compiler.backends.native.llvm.shim_path --> dist.payload.assemble.assemble_site { write_shim_record }
    compiler.backends.native.llvm.binding.common --> compiler.backends.native.llvm.binding.dylib { _encode_string }
    compiler.backends.native.llvm.binding.common --> compiler.backends.native.llvm.binding.ffi { _is_shutting_down }
    compiler.backends.native.llvm.binding.common --> compiler.backends.native.llvm.binding.module { _decode_string, _encode_string }
    compiler.backends.native.llvm.binding.common --> compiler.backends.native.llvm.binding.options { _encode_string }
    compiler.backends.native.llvm.binding.common --> compiler.backends.native.llvm.binding.targets { _decode_string, _encode_string }
    compiler.backends.native.llvm.binding.common --> compiler.backends.native.llvm.binding.value { _decode_string, _encode_string }
    include compiler.backends.native.llvm.binding.config --> compiler.backends.native.llvm.binding;
    compiler.backends.native.llvm.binding.config --> compiler.backends.native.llvm.binding.targets { _has_svml as has_svml }
    include compiler.backends.native.llvm.binding.context --> compiler.backends.native.llvm.binding;
    compiler.backends.native.llvm.binding.context --> compiler.backends.native.llvm.binding.module { get_global_context }
    include compiler.backends.native.llvm.binding.dylib --> compiler.backends.native.llvm.binding;
    type compiler.backends.native.llvm.binding.executionengine --> cli.commands.execution { ExecutionEngine }
    include compiler.backends.native.llvm.binding.executionengine --> compiler.backends.native.llvm.binding;
    include compiler.backends.native.llvm.binding.initfini --> compiler.backends.native.llvm.binding;
    compiler.backends.native.llvm.binding.initfini --> compiler.backends.native.llvm.binding.targets { llvm_version_info }
    include compiler.backends.native.llvm.binding.linker --> compiler.backends.native.llvm.binding;
    compiler.backends.native.llvm.binding.linker --> compiler.backends.native.llvm.binding.module { link_modules }
    include compiler.backends.native.llvm.binding.module --> compiler.backends.native.llvm.binding;
    include compiler.backends.native.llvm.binding.newpassmanagers --> compiler.backends.native.llvm.binding;
    include compiler.backends.native.llvm.binding.object_file --> compiler.backends.native.llvm.binding;
    include compiler.backends.native.llvm.binding.options --> compiler.backends.native.llvm.binding;
    include compiler.backends.native.llvm.binding.targets --> compiler.backends.native.llvm.binding;
    type compiler.backends.native.llvm.binding.value --> compiler.backends.native.link_plan { ValueRef }
    compiler.backends.native.llvm.binding.value --> compiler.backends.native.link_plan.internalize_native_implementation { Visibility }
    include compiler.backends.native.llvm.binding.value --> compiler.backends.native.llvm.binding;
    compiler.backends.native.llvm.binding.value --> compiler.backends.native.llvm.binding.module { ValueRef }
    type compiler.backends.native.llvm.binding.value --> compiler.backends.native.llvm.binding.targets { ValueRef }
    compiler.backends.native.llvm.binding.value --> compiler.backends.native.llvm.binding.targets.TargetMachine.emit_object { Linkage }
    include compiler.backends.native.llvm.ir.builder --> compiler.backends.native.llvm.ir;
    compiler.backends.native.llvm.ir.context --> compiler.backends.native.llvm.ir { Context, global_context }
    include compiler.backends.native.llvm.ir.instructions --> compiler.backends.native.llvm.ir;
    include compiler.backends.native.llvm.ir.module --> compiler.backends.native.llvm.ir;
    compiler.backends.native.llvm.ir.module --> compiler.backends.native.llvm.ir.instructions { Module }
    compiler.backends.native.llvm.ir.types --> compiler.backends.native.link_glue.bind_shared_callbacks { _wrapname }
    include compiler.backends.native.llvm.ir.types --> compiler.backends.native.llvm.ir;
    include compiler.backends.native.llvm.ir.values --> compiler.backends.native.llvm.ir;
    compiler.backends.native.llvm.ir.values --> compiler.backends.native.llvm.ir.builder { Value }
    compiler.backends.native.llvm.ir.values --> compiler.backends.native.llvm.ir.instructions { ArgumentAttributes, AttributeSet, Block, Constant, Function, MetaDataArgument, MetaDataString, NamedValue, Value }
    compiler.backends.native.llvm.ir._utils as _utils --> compiler.backends.native.llvm.ir.context;
    compiler.backends.native.llvm.ir._utils as _utils --> compiler.backends.native.llvm.ir.module;
    compiler.backends.native.llvm.ir._utils as _utils --> compiler.backends.native.llvm.ir.values;
    compiler.backends.native.llvm.ir.context --> compiler.backends.native.llvm.ir.module { Context, global_context }
    type compiler.backends.native.llvm.ir.context --> compiler.backends.native.llvm.ir.types { Context }
    compiler.backends.native.llvm.ir.instructions as instructions --> compiler.backends.native.llvm.ir.builder;
    compiler.backends.native.llvm.ir.instructions --> compiler.backends.native.llvm.ir.values.Block.replace { Instruction }
    type compiler.backends.native.llvm.ir.module --> compiler.backends.native.llvm.ir.builder { Module }
    type compiler.backends.native.llvm.ir.module --> compiler.backends.native.llvm.ir.values { Module }
    compiler.backends.native.llvm.ir.types as types --> compiler.backends.native.llvm.ir.builder;
    compiler.backends.native.llvm.ir.types as types --> compiler.backends.native.llvm.ir.context;
    compiler.backends.native.llvm.ir.types as types --> compiler.backends.native.llvm.ir.instructions;
    compiler.backends.native.llvm.ir.types as types --> compiler.backends.native.llvm.ir.module;
    compiler.backends.native.llvm.ir.types as types --> compiler.backends.native.llvm.ir.values;
    compiler.backends.native.llvm.ir.values as values --> compiler.backends.native.llvm.ir.builder;
    compiler.backends.native.llvm.ir.values --> compiler.backends.native.llvm.ir.instructions { _str_list, _value_list }
    compiler.backends.native.llvm.ir.values as values --> compiler.backends.native.llvm.ir.module;
    type compiler.backends.native.llvm.ir.values --> compiler.backends.native.llvm.ir.types { Constant, Value }
    compiler.backends.native.llvm.ir.values --> compiler.backends.native.llvm.ir.types.ArrayType.wrap_constant_value { Constant, Value }
    compiler.backends.native.llvm.ir.values --> compiler.backends.native.llvm.ir.types.BaseStructType.gep { Constant }
    compiler.backends.native.llvm.ir.values --> compiler.backends.native.llvm.ir.types.Type.__call__ { Constant }
    compiler.backends.native.llvm.ir.values --> compiler.backends.native.llvm.ir.types.VectorType.wrap_constant_value { Constant }
    compiler.backends.native.llvm.ir.values --> compiler.backends.native.llvm.ir.types._format_members { Value }
    compiler.backends.native.llvm.ir.values --> compiler.backends.native.llvm.ir.types._wrap_members { Constant, Value }
    compiler.backends.py.artifact_imports --> compiler.driver.application._prepare { package_sources, runtime_sources }
    compiler.backends.py.artifact_imports --> compiler.driver.application._prepare_sealed { package_sources, runtime_sources }
    compiler.backends.py.artifact_imports --> dist.precompile_bytecode.seal_runtime_closure { runtime_sources }
    compiler.backends.py.codegen_ir --> compiler.backends.py.codegen_shim { CirContainer, CirDiag, CirModule, CodegenIrFormatError, CodegenIrVersionError, DIAG_ERROR, OP_BYTES, OP_ELLIPSIS, OP_END, OP_FALSE, OP_FLOAT, OP_INT, OP_INT_BIG, OP_LIST, OP_LOC, OP_NODE, OP_NONE, OP_PARSE_SPLICE, OP_STR, OP_TRUE, OP_TUPLE, _r_svarint, _r_varint, read_container }
    compiler.backends.py.codegen_ir --> compiler.backends.py.jcir_gen_pass { CodegenIrWriter }
    compiler.backends.py.codegen_shim --> compiler.backends.py.jcir_bc_gen_pass.JcirBytecodeGenPass.transcribe_module { compile_ir }
    compiler.backends.py.jcir_facts --> compiler.backends.py.codegen_ir { jcir_python_version }
    compiler.backends.py.jcir_facts --> compiler.backends.py.jcir_gen_pass { JCIR_AMBIENT_TYPING_NAMES, JCIR_BUILTIN_NAMES, jcir_is_test_path }
    compiler.backends.py.artifact_imports --> compiler.driver.pipeline_runner.compile_application { package_sources }
    compiler.backends.py.codegen_shim --> cli.commands.transform.jac2py | cli.mcp.compiler_bridge.CompilerBridge.jac_to_py._do_jac2py | compiler.driver.source_products.python_source { generated_python }
    compiler.backends.py.codegen_shim --> compiler.tools.lang_tools.AstTool.ir { generated_python }
    compiler.backends.py.artifact_imports --> compiler.driver.application._reusable_interfaces { resolve_imports }
    compiler.backends.py.artifact_imports --> compiler.driver.application._prepare_revision { package_sources }
    compiler.backends.py.codegen_ir --> compiler.backends.py.jcir_gen_pass { int_literal_magnitude }
    compiler.backends.py.codegen_shim --> compiler.driver.compiler.assemble_jcir { compile_ir }
    compiler.backends.py.jcir_gen_pass --> compiler.driver.module_compile { JcirGenPass }
    compiler.backends.py.artifact_imports --> compiler.driver.application._prepare_revision { import_specs, resolve_imports }
    compiler.backends.py.jcir_bc_gen_pass --> compiler.driver.pipeline.bytecode_passes { JcirBytecodeGenPass }
    compiler.backends.py.jcir_gen_pass --> compiler.driver.pipeline.py_ir_passes { JcirGenPass }
    compiler.driver.jir --> project.compiler_host._wiring_records_path { get_jir_cache_dir, running_compiler_digest }
    compiler.driver.application --> cli.commands.execution.serve { prepare_application }
    compiler.driver.application --> client.targets.client_dev_common.dev_proxy_paths { prepare_application }
    compiler.driver.application --> compiler.driver.build_services.CompilerBuildServices.prepare_application { prepare_application }
    compiler.driver.application --> dist.seal.build_serve_manifest { prepare_application }
    compiler.driver.application --> dist.source.project.export_project { prepare_application }
    compiler.driver.application --> scale.server.inprocess.prepare_inprocess_runtime { prepare_application }
    compiler.driver.application --> scale.tests.data.test_eager_spawn { prepare_application }
    compiler.driver.application --> scale.tests.microservices.test_microservice { prepare_application }
    compiler.driver.application --> scale.tests.server.test_host_serving { prepare_application }
    compiler.driver.application --> scale.tests.server.test_served_app_route { prepare_application }
    compiler.driver.application --> scale.tests.server.test_sv_outbox_endpoints { prepare_application }
    compiler.driver.application --> server.hmr.HotReloader._reload_server_module { reprepare_application }
    compiler.driver.application_edges --> compiler.driver.build_services.CompilerBuildServices.application_edges { application_edges }
    compiler.driver.bccache --> cli.commands.analysis._check_file_job { discover_base_file }
    compiler.driver.bccache --> cli.commands.analysis._drop_covered_annexes { discover_base_file }
    compiler.driver.bccache --> cli.commands.analysis._format_single_file_worker { discover_annex_files }
    compiler.driver.bccache --> cli.commands.analysis.lint.lint_fix_file { discover_annex_files }
    compiler.driver.bccache --> cli.commands.analysis.precommit { discover_annex_files }
    compiler.driver.bccache --> cli.commands.architecture { discover_annex_files }
    compiler.driver.bccache --> compiler.driver.ifacecache.IfaceRegistry._entry_fresh { discover_annex_files }
    compiler.driver.bccache --> compiler.driver.jir._related_files { discover_annex_files }
    compiler.driver.bccache --> compiler.tests.test_batch_decl_identity { discover_base_file }
    compiler.driver.bccache --> compiler.tests.test_global_narrowing { discover_base_file }
    compiler.driver.bccache --> compiler.tools.code_intel { discover_annex_files }
    compiler.driver.bccache --> lsp.server.engine { discover_annex_files, discover_base_file }
    compiler.driver.bccache --> server.hmr { discover_base_file }
    compiler.driver.bccache --> testing.test_runner._suite_source { discover_base_file }
    compiler.driver.boundary_classify --> compiler.backends.es.esast_gen_pass.EsastGenPass._is_client_native_import { import_binds_client_native }
    compiler.driver.boundary_classify --> compiler.backends.es.esast_gen_pass.EsastGenPass._is_service_bridge_import { CrossAppKind, classify_cross_app_import }
    compiler.driver.boundary_classify --> compiler.backends.es.esast_gen_pass.EsastGenPass._partition_client_import_items { import_crosses_apps }
    compiler.driver.boundary_classify --> compiler.backends.es.esast_gen_pass.EsastGenPass._record_sv_backend { import_crosses_apps, import_provider_app, import_provider_route }
    compiler.driver.boundary_classify --> compiler.backends.es.esast_gen_pass.EsastGenPass._sv_provider_options { import_crosses_apps, import_provider_app, import_provider_route }
    compiler.driver.boundary_classify --> compiler.backends.py.jcir_gen_pass.JcirGenPass._generate_sv_to_sv_stubs { import_provider_app, import_provider_route }
    compiler.driver.boundary_classify --> compiler.backends.py.jcir_gen_pass.JcirGenPass._sv_bridge_walker_call { CrossAppKind, classify_cross_app_import }
    compiler.driver.boundary_classify --> compiler.backends.py.jcir_gen_pass.JcirGenPass._sv_consumer_app_expr { module_app }
    compiler.driver.boundary_classify --> compiler.backends.py.jcir_gen_pass.JcirGenPass.exit_import { CrossAppKind, classify_cross_app_import, import_binds_client_native }
    compiler.driver.boundary_classify --> compiler.frontend.unitree.Import.is_service_import.getter { is_service_bridge_import }
    compiler.driver.boundary_classify --> compiler.passes.access_check_pass.AccessCheckPass._collect_bridged_imports { classify_cross_app_import }
    compiler.driver.boundary_classify --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._bridge_targets { bridgeable_import_target, import_provider_app, module_app }
    compiler.driver.boundary_classify --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._check_app_cycle { bridgeable_import_target }
    compiler.driver.boundary_classify --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._check_provider_pub { ClientImportVerdict, classify_client_import_item, import_provider_app, module_app }
    compiler.driver.boundary_classify --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._parsed_provider_of { bridgeable_import_target }
    compiler.driver.boundary_classify --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._provider_module_of { bridgeable_import_target, symbol_linked_source_module }
    compiler.driver.boundary_classify --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._record_app_edge { import_provider_app, module_app }
    compiler.driver.boundary_classify --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._register_client_bridged_import { ClientImportVerdict, classify_client_import_item, import_crosses_apps, import_provider_app, import_provider_route, is_client_boundary_import }
    compiler.driver.boundary_classify --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._register_sv_import { import_crosses_apps, import_provider_app, import_provider_route }
    compiler.driver.boundary_classify --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._register_type_import { import_provider_app }
    compiler.driver.boundary_classify --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._reject_owned_type_import { import_provider_app, module_app }
    compiler.driver.boundary_classify --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass.enter_import { CrossAppKind, classify_cross_app_import }
    compiler.driver.boundary_classify --> compiler.passes.static_analysis_pass.StaticAnalysisPass._check_client_imports { is_client_native_edge_import }
    compiler.driver.boundary_classify --> compiler.passes.wasm_contract.host_contracts { symbol_linked_source_module }
    compiler.driver.boundary_classify --> compiler.placement.placement._element_reqs { classify_import }
    compiler.driver.boundary_classify --> compiler.placement.placement.module_anchor_reasons { ability_delegates_to_model, classify_import, is_service_app_entry }
    compiler.driver.boundary_classify --> compiler.placement.placement_facts.discover_spaces { hub_module_for_path }
    compiler.driver.boundary_classify --> compiler.placement.placement_solver._closure_pullable { is_server_anchored_module }
    compiler.driver.boundary_classify --> compiler.placement.placement_solver._is_sv_import { import_crosses_apps }
    compiler.driver.boundary_classify --> compiler.placement.placement_solver._materialize_module { hub_module_for_path }
    compiler.driver.boundary_classify --> compiler.placement.placement_solver._pull_boundary_import { plain_native_import_target }
    compiler.driver.boundary_classify --> compiler.placement.placement_solver._pullable_by_client_reference { is_server_anchored_module }
    compiler.driver.boundary_classify --> compiler.placement.placement_solver._seed_from_summary { _stamp_context_element }
    compiler.driver.boundary_classify --> compiler.placement.placement_solver.solve_module_placement { _stamp_context_element }
    compiler.driver.boundary_classify --> compiler.symbol_utils { ClientImportVerdict, classify_client_import_item, is_client_boundary_import, symbol_linked_source_module }
    compiler.driver.boundary_classify --> compiler.types.type_evaluator.TypeEvaluator._is_sv_async_call { CrossAppKind, classify_cross_app_import, is_client_native_edge_import }
    compiler.driver.compilation_context --> compiler.driver.application._prepare { cache_scope, program_for }
    compiler.driver.compilation_context --> compiler.driver.application._sections { cache_scope, program_for }
    compiler.driver.compilation_context --> compiler.driver.application._semantic_metadata { program_for }
    compiler.driver.compilation_context --> compiler.driver.application.prepare_application { bind_options, context_program }
    compiler.driver.compilation_context --> compiler.driver.application.prepare_dynamic_module { program_for }
    compiler.driver.compilation_context --> compiler.driver.compiler.JacCompiler.compile { bind_options, compilation_scope, context_program }
    compiler.driver.compilation_context --> compiler.driver.compiler.JacCompiler.get_bytecode { bind_options, compilation_scope, context_program }
    compiler.driver.compilation_context --> compiler.driver.compiler.JacCompiler.get_client_artifact { bind_options, compilation_scope, context_program }
    compiler.driver.compilation_context --> compiler.driver.ifacecache.IfaceRegistry._compilation_scope { compilation_scope }
    compiler.driver.compilation_context --> compiler.driver.ifacecache.IfaceRegistry.ensure { program_for }
    compiler.driver.compilation_context --> compiler.driver.jir.compute_precompile_module_key { cache_scope }
    compiler.driver.compilation_context --> compiler.driver.nativecache.NativeUnitRegistry._source_key { cache_scope }
    compiler.driver.compilation_context --> compiler.driver.program.JacProgram.load_dependency_module { program_for }
    compiler.driver.compilation_context --> compiler.driver.source_products.python_source { program_for }
    compiler.driver.compilation_context --> compiler.passes.access_check_pass.AccessCheckPass._module_app_facts { context_app }
    compiler.driver.compilation_context --> compiler.placement.placement_pins { context_app }
    compiler.driver.compilation_context --> dist.precompile_bytecode._application_sources { bind_options }
    compiler.driver.compilation_context --> dist.precompile_bytecode.precompile_context { bind_options, context_program }
    compiler.driver.compilation_context --> dist.precompile_bytecode.precompile_unit_context { cache_scope }
    compiler.driver.compile_options --> cli.commands.analysis._check_file_job { CompileOptions }
    compiler.driver.compile_options --> cli.commands.analysis.explain { CompileOptions }
    compiler.driver.compile_options --> cli.commands.analysis.grammar { CompileOptions }
    compiler.driver.compile_options --> cli.commands.execution._exec_file { CompileOptions, CompileOptions as _RunOpts }
    compiler.driver.compile_options --> cli.commands.native_build._restore_target { pop_native_target }
    compiler.driver.compile_options --> cli.commands.native_build.native_build { CompileOptions, NATIVE_LINK_MODES, pop_native_target, push_native_target }
    compiler.driver.compile_options --> compiler.backends.es.client_kernel_cache._lower { CompileOptions }
    compiler.driver.compile_options --> compiler.backends.native.elf_linker.ElfLinker.link { env_symmap_requested }
    compiler.driver.compile_options --> compiler.backends.native.kernel_resolve { CompileOptions, NATIVE_LINK_MODE_BITCODE }
    compiler.driver.compile_options --> compiler.backends.native.link_plan { CompileOptions, NATIVE_LINK_MODE_BITCODE, NATIVE_LINK_MODE_OBJECTS, env_na_debug }
    compiler.driver.compile_options --> compiler.backends.native.link_plan.build_link_plan { pop_native_target, push_native_target }
    compiler.driver.compile_options --> compiler.backends.native.llvm { env_typed_pointers_enabled }
    type compiler.driver.compile_options --> compiler.backends.native.na_compile_pass { CompileOptions }
    compiler.driver.compile_options --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._full_ast_of { env_na_debug }
    compiler.driver.compile_options --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._load_native_unit_module { CompileOptions as _UnitOpts }
    compiler.driver.compile_options --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._opaque_field_if_unlowerable { env_na_debug as _er_dbg }
    compiler.driver.compile_options --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._register_imported_struct_types { env_na_debug, env_na_debug as _ti_dbg }
    compiler.driver.compile_options --> compiler.driver.application.prepare_application { CompileOptions }
    compiler.driver.compile_options --> compiler.driver.application_edges.application_edges { CompileOptions }
    compiler.driver.compile_options --> compiler.driver.compilation_context { CompileOptions }
    compiler.driver.compile_options --> compiler.driver.compiler { CompileOptions }
    compiler.driver.compile_options --> compiler.driver.ifacecache.IfaceRegistry._ensure_in_context { CompileOptions }
    compiler.driver.compile_options --> compiler.driver.ifacecache.IfaceRegistry._verify_analysis { CompileOptions }
    compiler.driver.compile_options --> compiler.driver.ifacecache.IfaceRegistry._verify_iface { CompileOptions }
    compiler.driver.compile_options --> compiler.driver.jir._analysis_fingerprint_for { CompileOptions }
    compiler.driver.compile_options --> compiler.driver.nativecache { CompileOptions }
    compiler.driver.compile_options --> compiler.driver.nativecache.NativeBuildSession.finish { pop_native_target, push_native_target }
    compiler.driver.compile_options --> compiler.driver.nativecache.NativeBuildSession.lower { env_na_debug, pop_native_target, push_native_target }
    compiler.driver.compile_options --> compiler.driver.nativecache.NativeUnitRegistry._source_key { pop_native_target, push_native_target }
    compiler.driver.compile_options --> compiler.driver.nativecache.NativeUnitRegistry.known_digest { env_na_debug }
    compiler.driver.compile_options --> compiler.driver.pipeline_runner { CompileOptions }
    compiler.driver.compile_options --> compiler.driver.pipeline_runner.native_application { CompileOptions, pop_native_target, push_native_target }
    compiler.driver.compile_options --> compiler.driver.pipeline_runner.wasm_ir { CompileOptions, pop_native_target, push_native_target }
    compiler.driver.compile_options --> compiler.driver.program { CompileOptions }
    compiler.driver.compile_options --> compiler.tests.test_batch_decl_identity { CompileOptions }
    compiler.driver.compile_options --> compiler.tests.test_client_codegen_facts { CompileOptions }
    compiler.driver.compile_options --> compiler.tests.test_global_narrowing { CompileOptions }
    compiler.driver.compile_options --> compiler.tests.test_graph_fragment_equivalence { CompileOptions }
    compiler.driver.compile_options --> compiler.tests.test_missing_local_import { CompileOptions }
    compiler.driver.compile_options --> compiler.tests.test_native_kernel_cache { CompileOptions }
    compiler.driver.compile_options --> compiler.tests.test_stubcat_roundtrip { CompileOptions }
    compiler.driver.compile_options --> compiler.tests.test_subscript_assignment { CompileOptions }
    compiler.driver.compile_options --> compiler.tests.test_tarfile_equivalence { CompileOptions }
    compiler.driver.compile_options --> compiler.tests.test_unknown_cascade { CompileOptions }
    compiler.driver.compile_options --> compiler.tests.test_zstd_equivalence { CompileOptions }
    compiler.driver.compile_options --> compiler.tests.xbackend_equiv { CompileOptions }
    compiler.driver.compile_options --> compiler.tools.code_intel.CodeIntelligence._full_compile_one { CompileOptions }
    compiler.driver.compile_options --> compiler.tools.lang_tools { CompileOptions }
    compiler.driver.compile_options --> dist.precompile_bytecode._application_sources { CompileOptions }
    compiler.driver.compile_options --> dist.precompile_bytecode.precompile_context { CompileOptions }
    compiler.driver.compile_options --> dist.precompile_bytecode.precompile_native_unit { CompileOptions }
    compiler.driver.compile_options --> dist.precompile_bytecode.seal_native { CompileOptions }
    compiler.driver.compile_options --> dist.publish.builder._module_is_client_source { CompileOptions }
    compiler.driver.compile_options --> dist.publish.npm_sources._compile_module { CompileOptions }
    compiler.driver.compile_options --> lsp.server.engine.JacLangServer.type_check_file { CompileOptions }
    compiler.driver.compile_options --> testing.cl_test_runner.module_is_client { CompileOptions }
    compiler.driver.compiler --> cli.mcp.compiler_bridge.CompilerBridge.lint_snippet._do_lint { JacCompiler }
    type compiler.driver.compiler --> compiler.driver.build_services { JacCompiler }
    compiler.driver.compiler --> compiler.driver.build_services.CompilerBuildServices.compiler { JacCompiler }
    type compiler.driver.compiler --> compiler.driver.program { JacCompiler }
    compiler.driver.compiler --> compiler.driver.program.JacProgram._get_compiler { JacCompiler }
    compiler.driver.compiler --> compiler.driver.program.JacProgram.jac_file_formatter { JacCompiler }
    compiler.driver.compiler --> compiler.driver.program.JacProgram.jac_file_linter { JacCompiler }
    compiler.driver.compiler --> compiler.driver.program.JacProgram.jac_str_formatter { JacCompiler }
    compiler.driver.compiler --> compiler.types.stubcat.build.build_catalog { JacCompiler }
    compiler.driver.compiler --> dist.precompile_bytecode.run_precompile { COMPILE_GC_THRESHOLDS }
    type compiler.driver.compiler --> runtime.build_services { JacCompiler }
    type compiler.driver.compiler --> runtime.runtime { JacCompiler }
    compiler.driver.context_passes --> compiler.driver.pipeline { AbsorbImportsPass, AppContextPass, BoundaryFactsPass }
    compiler.driver.dependency_graph --> compiler.backends.native.link_plan._build_link_plan { dependency_groups }
    compiler.driver.ifacecache --> compiler.driver.program.JacProgram.iface_registry { IfaceRegistry }
    compiler.driver.ifacecache --> dist.precompile_bytecode._unit_extra { DIAG_SCHEMA, IfaceRegistry }
    compiler.driver.ifacecache --> lsp.server.engine.JacLangServer._fanout_dependents { seed_dep_edges }
    compiler.driver.jir --> byllm.tests.test_mtir_integration { HEADER_SIZE, SECTIONS_MAGIC, SEC_BYTECODE, SEC_MTIR, get_module_cache_path, read_sections, write_sections }
    compiler.driver.jir --> cli.commands.cache._live_keys { compiler_generation }
    compiler.driver.jir --> cli.commands.execution._exec_file { scrub_cache_dirs }
    compiler.driver.jir --> compiler.backends.es.client_kernel_cache._artifact_path { running_compiler_digest }
    compiler.driver.jir --> compiler.backends.native.link_plan { sidecar_unit_paths, unit_source_digest }
    compiler.driver.jir --> compiler.backends.native.link_plan._build_link_plan.walk_unit { module_cache_key }
    compiler.driver.jir --> compiler.backends.native.link_plan._reuse_artifact { cache_mode }
    compiler.driver.jir --> compiler.backends.native.na_compile_pass.NativeCompilePass._emit_debug_products { get_native_debug_dir }
    compiler.driver.jir --> compiler.driver.application._context_sections { HEADER_SIZE, SECTIONS_MAGIC, get_module_cache_path, read_sections }
    compiler.driver.jir --> compiler.driver.application._identity { compiler_generation }
    compiler.driver.jir --> compiler.driver.application._prepare { cache_mode }
    compiler.driver.jir --> compiler.driver.application._prepare_sealed { HEADER_SIZE, PRECOMPILE_SENTINEL, SECTIONS_MAGIC, patch_co_filenames_bytes, read_bytecode_only, read_sections }
    compiler.driver.jir --> compiler.driver.compiler { FLAG_PRECOMPILED, HEADER_SIZE, SECTIONS_MAGIC, SEC_BYTECODE, SEC_CLIENT, SEC_INTEROP, SEC_MTIR, SEC_NBITCODE, SEC_NOBJ, SEC_PLACEMENT, cache_mode, compute_content_sha256, get_module_cache_path, is_module_cache_valid, patch_co_filenames_bytes, precompiled_jir_matches_source, read_bytecode_only, read_section_bytes, read_sections, write_module_cache }
    compiler.driver.jir --> compiler.driver.compiler.JacCompiler._get_bytecode { PRECOMPILE_SENTINEL, SEC_CTDEPS as _PC_CTDEPS }
    compiler.driver.jir --> compiler.driver.compiler.JacCompiler._get_precompiled_jir_bytecode { PRECOMPILE_SENTINEL, SEC_CTDEPS, absolutize_ct_deps_section, bundle_dir_allowed, cache_mode }
    compiler.driver.jir --> compiler.driver.compiler.JacCompiler._persist_module_cache { get_module_cache_path, is_module_cache_valid }
    compiler.driver.jir --> compiler.driver.compiler.JacCompiler._precompiled_jir_data { bundle_dir_allowed, cache_mode, precompiled_jir_matches_source }
    compiler.driver.jir --> compiler.driver.compiler.JacCompiler._restore_sections { JirPaths, SEC_PATH_ROOT }
    compiler.driver.jir --> compiler.driver.ifacecache { DepRow, JirPaths, SEC_CTDEPS, SEC_DEPS, SEC_DIAG, SEC_IFACE, SEC_PATH_ROOT, SEC_PLACEMENT, cache_mode, deps_section, get_module_cache_path, is_compiler_tree_path, is_module_cache_valid, is_stub_like_path, jir_cacheable_source_path, module_cache_key, read_dep_hashes, read_jir_paths, read_section_bytes, write_module_cache }
    compiler.driver.jir --> compiler.driver.ifacecache.IfaceRegistry._deps_match { compute_stub_module_key, read_dep_rows }
    compiler.driver.jir --> compiler.driver.ifacecache.IfaceRegistry._persist_in_context { SEC_INTEROP }
    compiler.driver.jir --> compiler.driver.ifacecache.IfaceRegistry.client_boundary_facts { SEC_INTEROP, read_dep_rows }
    compiler.driver.jir --> compiler.driver.ifacecache.IfaceRegistry.note_dep { compute_stub_module_key }
    compiler.driver.jir --> compiler.driver.nativecache { NativeStamp, SEC_NBITCODE, SEC_NCTDEPS, SEC_NIFACE, SEC_NOBJ, SEC_PLACEMENT, cache_mode, ct_dep_text_fresh, current_native_stamp, get_module_cache_path, is_module_cache_valid, jir_cacheable_source_path, module_cache_key, native_section_payload, read_native_dep_hashes, read_section_bytes }
    compiler.driver.jir --> compiler.driver.nativecache.NativeUnitRegistry.known_native_deps { read_dep_rows }
    compiler.driver.jir --> compiler.driver.nativecache.NativeUnitRegistry.object_for { write_module_cache }
    compiler.driver.jir --> compiler.driver.nativecache.NativeUnitRegistry.product_sections { SEC_NDEPS, absolutize_ct_deps_section, native_deps_section }
    compiler.driver.jir --> compiler.tools.code_intel { HEADER_SIZE, SECTIONS_MAGIC, SEC_SYMINDEX, create_header, get_module_cache_path, parse_header, read_sections, write_sections }
    compiler.driver.jir --> dist.payload.assemble.assemble_site { write_compiler_identity }
    compiler.driver.jir --> dist.precompile_bytecode { DepRow, FLAG_BOOTSTRAP, FLAG_PRECOMPILED, FORMAT_VERSION, HEADER_SIZE, NATIVE_SECTIONS, PRECOMPILE_SENTINEL, SECTIONS_MAGIC, SEC_BYTECODE, SEC_CTDEPS, SEC_DEBUG_SRC, SEC_DEPS, SEC_DIAG, SEC_IFACE, SEC_MODKEY, SEC_NIFACE, SEC_NOBJ, SEC_PATH_ROOT, SEC_PLACEMENT, compute_precompile_module_key, deps_section, get_module_cache_path, is_module_cache_valid, parse_header, patch_co_filenames_bytes, precompiled_jir_matches_source, read_dep_rows, read_jir_paths, read_section_bytes, read_sections, rebase_ct_deps_section, running_compiler_digest, write_precompiled_jir }
    compiler.driver.jir --> dist.precompile_bytecode._native_extra { NativeStamp, SEC_NCTDEPS, native_section_variants, pack_native_variants, rebase_placement_section }
    compiler.driver.jir --> dist.precompile_bytecode._precompile_unit { cache_mode }
    compiler.driver.jir --> dist.precompile_bytecode.run_precompile { read_debug_source }
    compiler.driver.jir --> dist.precompile_bytecode.seal_native { native_section_payload, read_section_bytes as _rsb }
    compiler.driver.jir as jir --> scale.tests.microservices.test_seed_determinism;
    compiler.driver.jir --> scale.tests.microservices.test_seed_determinism { FLAG_PRECOMPILED, compiler_source_digest, compiler_source_files, compute_module_key, compute_precompile_module_key, module_cache_key, precompiled_jir_matches_source, running_compiler_digest, write_precompiled_jir }
    compiler.driver.na_coverage --> cli.commands.analysis._check_file_job { na_coverage_begin }
    compiler.driver.na_coverage --> cli.commands.analysis.check { na_coverage_end }
    compiler.driver.na_coverage --> compiler.backends.native.link_plan._build_link_plan { na_coverage_replay }
    compiler.driver.na_coverage --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._export_native_iface { na_coverage_capture }
    compiler.driver.na_coverage --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._opaque_field_if_unlowerable { na_coverage_seam }
    compiler.driver.na_coverage --> compiler.driver.pipeline_runner.wasm_ir { na_coverage_begin, na_coverage_end }
    compiler.driver.native_iface --> compiler.backends.native.link_plan { NativeIface, layout_digest as layout_digest_of, merge_class_layouts }
    compiler.driver.native_iface --> compiler.backends.native.na_ir_gen_pass { NativeExport, NativeIface }
    compiler.driver.native_iface --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._export_native_iface { NativeClassLayout, NativeFieldSlot, NativeIface }
    compiler.driver.native_iface --> compiler.driver.nativecache { NativeIface }
    type compiler.driver.native_iface --> compiler.frontend.codeinfo { NativeIface }
    compiler.driver.native_iface --> compiler.tests.test_native_kernel_cache { NativeIface }
    compiler.driver.native_iface --> dist.precompile_bytecode.seal_native { NativeIface }
    compiler.driver.nativecache --> compiler.backends.native.link_plan.build_link_plan { NativeBuildSession }
    type compiler.driver.nativecache --> compiler.driver.program { NativeUnitRegistry }
    compiler.driver.nativecache --> compiler.driver.program.JacProgram.native_units { NativeUnitRegistry }
    compiler.driver.nativecache --> compiler.tests.test_native_kernel_cache { NativeUnitEntry }
    compiler.driver.pass_driver --> compiler.driver.application.prepare_application { compile_progress }
    compiler.driver.pass_driver --> compiler.driver.ifacecache.IfaceRegistry.analysis_profile { diagnostic_policy_for }
    compiler.driver.pass_driver --> compiler.driver.pipeline.execute_passes { build_diagnostic_policy, run_pass }
    compiler.driver.pass_driver --> compiler.tests.test_client_codegen_facts { run_pass }
    compiler.driver.pass_driver as pass_driver --> compiler.tests.test_pipeline_products;
    compiler.driver.pass_driver --> compiler.tools.jac_auto_lint_pass.JacAutoLintPass.__post_init__ { diagnostic_policy_for }
    compiler.driver.pipeline --> compiler.backends.es.client_kernel_cache._lower { CompilationProduct }
    compiler.driver.pipeline --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._ensure_dep_inference { CompilationProduct }
    compiler.driver.pipeline --> compiler.driver.application_edges.application_edges { CompilationProduct }
    compiler.driver.pipeline --> compiler.passes.layout_pass.get_layout_registry { CompilationProduct }
    compiler.driver.pipeline --> compiler.tests.test_pipeline_products { product_ready }
    compiler.driver.pipeline --> compiler.tools.lang_tools { CompilationProduct }
    compiler.driver.pipeline --> dist.publish.npm_sources._compile_module { CompilationProduct }
    compiler.driver.pipeline_runner --> dist.source.client.write_client { wasm_ir }
    compiler.driver.pipeline_runner --> dist.source.project.export_project { native_application }
    compiler.driver.pipeline_types --> compiler.backends.native.na_ir_gen_pass { AnalysisFact }
    compiler.driver.pipeline_types --> compiler.driver.compiler { AnalysisFact }
    compiler.driver.pipeline_types --> compiler.driver.ifacecache { AnalysisFact }
    compiler.driver.pipeline_types --> compiler.driver.nativecache.NativeBuildSession.lower { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.driver.pipeline { AnalysisFact, CompilationProduct, PassContract, ProductTask, TaskState }
    compiler.driver.pipeline_types --> compiler.driver.program { AnalysisFact }
    compiler.driver.pipeline_types --> compiler.driver.progstate { AnalysisFact, CompilationProduct, ProductTask }
    compiler.driver.pipeline_types --> compiler.tests.test_pipeline_products { AnalysisFact, ProductTask, TaskState }
    compiler.driver.program --> byllm.tests.test_byllm { JacProgram }
    compiler.driver.program --> byllm.tests.test_mtir_integration { JacProgram }
    compiler.driver.program --> cli.commands.analysis._check_file_job { JacProgram }
    compiler.driver.program --> cli.commands.analysis._format_single_file_worker { JacProgram }
    compiler.driver.program --> cli.commands.analysis.explain { JacProgram }
    compiler.driver.program --> cli.commands.analysis.grammar { JacProgram }
    compiler.driver.program --> cli.commands.analysis.lint { JacProgram }
    compiler.driver.program --> cli.commands.architecture { JacProgram }
    compiler.driver.program --> cli.commands.execution.debug { JacProgram }
    compiler.driver.program --> cli.commands.fix._format_source { JacProgram }
    compiler.driver.program --> cli.commands.fix._verify_claims { JacProgram }
    compiler.driver.program --> cli.commands.native_build.native_build { JacProgram }
    compiler.driver.program --> cli.commands.transform.jac2js { JacProgram }
    compiler.driver.program --> cli.commands.transform.jac2py { JacProgram }
    compiler.driver.program --> cli.commands.transform.py2jac { JacProgram }
    compiler.driver.program --> cli.mcp.compiler_bridge.CompilerBridge.get_ast_snippet._do_ast { JacProgram }
    compiler.driver.program --> cli.mcp.compiler_bridge.CompilerBridge.jac_to_js._do_jac2js { JacProgram }
    compiler.driver.program --> cli.mcp.compiler_bridge.CompilerBridge.jac_to_py._do_jac2py { JacProgram }
    compiler.driver.program --> cli.mcp.compiler_bridge.CompilerBridge.parse_snippet._do_parse { JacProgram }
    compiler.driver.program --> cli.mcp.compiler_bridge.CompilerBridge.py_to_jac._do_py2jac { JacProgram }
    compiler.driver.program --> cli.mcp.compiler_bridge.CompilerBridge.typecheck_snippet._do_typecheck { JacProgram }
    type compiler.driver.program --> client.client_bundle { JacProgram }
    type compiler.driver.program --> client.compiler { JacProgram }
    type compiler.driver.program --> client.vite_client_bundle { JacProgram }
    compiler.driver.program --> compiler.backends.es.client_kernel_cache._lower { JacProgram }
    compiler.driver.program --> compiler.backends.native.kernel_resolve.kernel_plan { JacProgram }
    type compiler.driver.program --> compiler.backends.native.link_plan { JacProgram }
    compiler.driver.program --> compiler.backends.native.wasm_build.compile_to_wasm { JacProgram }
    compiler.driver.program --> compiler.driver.application_edges.application_edges { JacProgram }
    compiler.driver.program --> compiler.driver.boundary_classify { JacProgram }
    type compiler.driver.program --> compiler.driver.build_services { JacProgram }
    compiler.driver.program --> compiler.driver.build_services.CompilerBuildServices.program { JacProgram }
    type compiler.driver.program --> compiler.driver.compilation_context { JacProgram }
    compiler.driver.program --> compiler.driver.compilation_context.context_program { JacProgram }
    compiler.driver.program --> compiler.driver.compiler { JacProgram }
    compiler.driver.program --> compiler.driver.compiler.JacCompiler._prepare_tool_program { JacProgram }
    compiler.driver.program --> compiler.driver.ifacecache.IfaceRegistry._fresh_verify_program { JacProgram }
    type compiler.driver.program --> compiler.driver.nativecache { JacProgram }
    compiler.driver.program --> compiler.driver.nativecache.NativeBuildSession.__post_init__ { JacProgram }
    compiler.driver.program --> compiler.driver.pass_driver { JacProgram }
    type compiler.driver.program --> compiler.driver.pipeline { JacProgram }
    compiler.driver.program --> compiler.driver.pipeline_runner { JacProgram }
    compiler.driver.program --> compiler.driver.selfhost { JacProgram }
    compiler.driver.program --> compiler.driver.source_failures { JacProgram }
    type compiler.driver.program --> compiler.driver.source_products { JacProgram }
    type compiler.driver.program --> compiler.frontend.parser.frontend { JacProgram }
    type compiler.driver.program --> compiler.passes.wasm_contract { JacProgram }
    compiler.driver.program --> compiler.placement.placement_facts.discover_spaces { JacProgram }
    type compiler.driver.program --> compiler.placement.placement_solver { JacProgram }
    compiler.driver.program --> compiler.placement.placement_solver._native_dep_scan { JacProgram }
    type compiler.driver.program --> compiler.symbol_utils { JacProgram }
    compiler.driver.program --> compiler.tests.test_batch_decl_identity { JacProgram }
    compiler.driver.program --> compiler.tests.test_client_codegen_facts { JacProgram }
    compiler.driver.program --> compiler.tests.test_client_npm_entry_root { JacProgram }
    compiler.driver.program --> compiler.tests.test_global_narrowing { JacProgram }
    compiler.driver.program --> compiler.tests.test_graph_fragment_equivalence { JacProgram }
    compiler.driver.program --> compiler.tests.test_jac_mobui_typing { JacProgram }
    compiler.driver.program --> compiler.tests.test_missing_local_import { JacProgram }
    compiler.driver.program --> compiler.tests.test_native_kernel_cache { JacProgram }
    compiler.driver.program --> compiler.tests.test_pipeline_products { JacProgram }
    compiler.driver.program --> compiler.tests.test_stubcat_roundtrip { JacProgram }
    compiler.driver.program --> compiler.tests.test_subscript_assignment { JacProgram }
    compiler.driver.program --> compiler.tests.test_tarfile_equivalence { JacProgram }
    compiler.driver.program --> compiler.tests.test_test_block_analysis { JacProgram }
    compiler.driver.program --> compiler.tests.test_unknown_cascade { JacProgram }
    compiler.driver.program --> compiler.tests.test_untyped_third_party { JacProgram }
    compiler.driver.program --> compiler.tests.test_zstd_equivalence { JacProgram }
    compiler.driver.program --> compiler.tests.xbackend_equiv { JacProgram }
    compiler.driver.program --> compiler.tools.code_intel { JacProgram }
    type compiler.driver.program --> compiler.tools.jac_auto_lint_pass { JacProgram }
    compiler.driver.program --> compiler.tools.jac_auto_lint_pass.JacAutoLintPass._base_decl_archetypes { JacProgram }
    compiler.driver.program --> compiler.tools.jac_formatter_pass.format_module { JacProgram }
    compiler.driver.program --> compiler.tools.lang_tools { JacProgram }
    type compiler.driver.program --> compiler.types.stubcat.build { JacProgram }
    compiler.driver.program --> compiler.types.stubcat.build.build_catalog { JacProgram }
    type compiler.driver.program --> compiler.types.type_evaluator { JacProgram }
    type compiler.driver.program --> dist.native_product { JacProgram }
    compiler.driver.program --> dist.native_product.write_native_product { JacProgram }
    type compiler.driver.program --> dist.precompile_bytecode { JacProgram }
    compiler.driver.program --> dist.precompile_bytecode._application_sources { JacProgram }
    compiler.driver.program --> dist.precompile_bytecode.precompile_native_unit { JacProgram }
    compiler.driver.program --> dist.precompile_bytecode.precompile_unit_context { JacProgram }
    compiler.driver.program --> dist.precompile_bytecode.seal_native { JacProgram }
    compiler.driver.program --> dist.precompile_bytecode.sealable_sources { JacProgram }
    type compiler.driver.program --> dist.publish.builder { JacProgram }
    compiler.driver.program --> dist.publish.builder.WheelBuilder._assemble_src_data { JacProgram as JacProgramRt }
    compiler.driver.program --> dist.publish.builder._module_is_client_source { JacProgram as JacProgramRt }
    compiler.driver.program --> dist.publish.npm_sources.collect_npm_sources { JacProgram }
    compiler.driver.program --> dist.publish.runtime_npm._compile_cl_to_js { JacProgram }
    compiler.driver.program --> dist.publish.runtime_vendor { JacProgram }
    compiler.driver.program --> dist.source.project { JacProgram }
    compiler.driver.program --> lsp.server.engine { JacProgram }
    compiler.driver.program --> lsp.server.module_manager { JacProgram }
    type compiler.driver.program --> runtime.build_services { JacProgram }
    type compiler.driver.program --> runtime.runtime { JacProgram }
    compiler.driver.program --> scale.tests.apps.test_fleet_from_apps { JacProgram }
    compiler.driver.program --> server.hmr.HotReloader._classify_declarations { JacProgram }
    compiler.driver.program --> testing.cl_test_runner.compile_cl_module { JacProgram }
    compiler.driver.program --> testing.cl_test_runner.module_is_client { JacProgram }
    compiler.driver.program --> testing.test_runner._fresh_jac_state { JacProgram }
    compiler.driver.progstate --> compiler.driver.program { AnalysisCaches, BuildScratch, DepGraph, DiagLedger, ModuleHub }
    type compiler.driver.selfhost --> compiler.driver.build_services { SelfHostCache }
    compiler.driver.selfhost --> compiler.driver.build_services.CompilerBuildServices.selfhost { SelfHostCache }
    compiler.driver.selfhost --> compiler.driver.compiler { SelfHostCache }
    compiler.driver.selfhost --> compiler.types.stubcat.build.build_catalog { SelfHostCache }
    type compiler.driver.selfhost --> runtime.build_services { SelfHostCache }
    type compiler.driver.selfhost --> runtime.runtime { SelfHostCache }
    compiler.driver.source_failures --> compiler.driver.application._prepare { bootstrap_tier_failure_details, module_scoped_failure_details }
    compiler.driver.source_failures --> compiler.driver.compiler { CompilerSourceError, bootstrap_tier_failure_details, import_error_re_enters, module_scoped_failure_details, note_compiler_source_failure }
    compiler.driver.source_failures --> compiler.driver.source_products.python_source { bootstrap_tier_failure_details, module_scoped_failure_details }
    compiler.driver.source_failures --> dist.precompile_bytecode._emit_unit_diagnostics { compiler_source_failure_details }
    compiler.driver.source_failures --> testing.cl_test_runner.module_is_client { CompilerSourceError, compiler_source_failure_origin }
    compiler.driver.source_products --> dist.publish.builder { python_source }
    compiler.driver.source_products --> dist.publish.runtime_vendor._compile_runtime_module { python_source }
    compiler.driver.source_products --> dist.source.project { python_source }
    compiler.driver.wiring --> cli.commands.architecture { ARCH_FILE_NAME, WireRec, arch_file_for, WiringSpec, scope_path_of, wiring_for_path }
    compiler.driver.wiring --> dist.precompile_bytecode.find_jac_files { is_arch_file }
    compiler.driver.wiring --> compiler.driver.jir.unit_source_digest { wiring_digest_for }
    compiler.driver.wiring --> compiler.frontend.parser.frontend.annex_sources { wiring_annex_for }
    compiler.driver.wiring --> compiler.passes.import_wiring_pass { RuleRec, WireBinding, WireRec, WiringSpec, pattern_text, is_arch_file, scope_owners, scope_path_of, wiring_for_path }
    compiler.driver.wiring --> compiler.tools.jac_auto_lint_pass { WiringSpec, compiled_by_seed, is_arch_file, scope_path_of, WireRec, wire_record, wiring_for_path }
    compiler.driver.bccache --> project.compiler_host.ProjectHost.annex_files { discover_annex_files }
    compiler.driver.bccache --> project.compiler_host.ProjectHost.base_file { discover_base_file }
    compiler.driver.bccache --> project.compiler_host.ProjectHost.is_annex_path_of { host_layout_tables }
    compiler.driver.bccache --> project.compiler_host.ProjectHost.package_init { host_layout_tables }
    compiler.driver.bccache --> project.compiler_host.ProjectHost.path_facts { host_layout_tables }
    compiler.driver.boundary_classify --> compiler.driver.program.JacProgram.declared_codespace { _default_codespace_for }
    compiler.driver.boundary_classify --> compiler.driver.program.JacProgram.infers_native_codespace { _default_codespace_for }
    compiler.driver.boundary_classify --> compiler.driver.program.JacProgram.parse_source { _coerce_client_module, _coerce_native_module }
    compiler.driver.boundary_classify --> compiler.driver.program.JacProgram.stamp_boundary_facts { ClientImportVerdict, _default_codespace_for, classify_client_import_item, import_declares_native_target, is_client_boundary_import, is_client_native_edge_import }
    compiler.driver.boundary_classify --> compiler.driver.program.JacProgram.stamp_native_import_facts { native_only_import_target }
    compiler.driver.client_graph --> client.jac_client_compiler.JacClientCompiler.emit_dependencies { collect_client_graph }
    compiler.driver.compilation_context --> compiler.driver.compiler.JacCompiler.get_bytecode | compiler.driver.ifacecache.IfaceRegistry._compilation_scope | dist.precompile_bytecode.precompile_unit_context { owner_scope_options }
    compiler.driver.compilation_context --> compiler.driver.compiler.JacCompiler.get_client_artifact { owner_scope_options }
    compiler.driver.compilation_context --> compiler.driver.compiler.JacCompiler.product_program | compiler.driver.pipeline_runner.compile_application | compiler.driver.session_compile.select_context { bind_options, context_program }
    compiler.driver.compilation_context --> compiler.driver.ifacecache.artifact_cache_path { cache_scope, program_for }
    compiler.driver.compilation_context --> compiler.driver.session_compile.compile_in_session { compilation_scope, owner_scope_options }
    compiler.driver.compilation_context --> compiler.frontend.kernel_host { package_owned }
    compiler.driver.compilation_context --> project.compiler_host.ProjectHost.drop_python_lane_products { cache_scope, owner_scope_options }
    compiler.driver.compilation_context --> project.compiler_host.ProjectHost.lint_settings { context_app }
    compiler.driver.compile_options --> compiler.backends.native.kernel_resolve { NATIVE_LINK_MODE_OBJECTS }
    compiler.driver.compile_options --> compiler.driver.module_analysis | compiler.driver.session_compile | compiler.frontend.kernel_host | compiler.frontend.kernel_inputs | dist.precompile_bytecode.prebuild_native_closure | dist.publish.runtime_vendor | dist.seal | project.kernel_check | project.kernel_snapshot { CompileOptions }
    compiler.driver.compile_options --> compiler.driver.pass_driver | compiler.passes.context | compiler.passes.execution | compiler.tests.test_pipeline_products | lsp.server.engine { CancelToken }
    type compiler.driver.compile_options --> compiler.driver.pipeline | compiler.driver.program { CancelToken }
    type compiler.driver.compile_options --> compiler.frontend.host | compiler.placement.placement_facts | project.compiler_host { CompileOptions }
    compiler.driver.compiler --> cli.commands.analysis.check { CHECK_GC_THRESHOLDS }
    compiler.driver.compiler --> project.compiler_host.ProjectHost.compiler_for { JacCompiler }
    compiler.driver.compiler --> project.compiler_host.ProjectHost.format_file { JacCompiler }
    compiler.driver.compiler --> project.compiler_host.ProjectHost.format_source { JacCompiler }
    compiler.driver.compiler --> project.compiler_host.ProjectHost.lint_file { JacCompiler }
    type compiler.driver.compiler --> compiler.frontend.host | compiler.frontend.kernel_host | project.compiler_host { JacCompiler }
    compiler.driver.ifacecache --> project.compiler_host.ProjectHost.iface_registry_for { IfaceRegistry }
    type compiler.driver.ifacecache --> compiler.driver.program | compiler.frontend.host | compiler.frontend.kernel_host | project.compiler_host { IfaceRegistry }
    compiler.driver.jir --> compiler.backends.native.link_plan._jit_image_path { cache_mode, get_jir_cache_dir }
    compiler.driver.jir --> compiler.driver.ifacecache.artifact_cache_path { get_module_cache_path }
    compiler.driver.jir --> project.compiler_host.ProjectHost.drop_python_lane_products { drop_python_lane_products }
    compiler.driver.jir --> project.kernel_snapshot.interface_cache_file { get_jir_cache_dir, running_compiler_digest }
    compiler.driver.module_analysis --> compiler.frontend.kernel_analyze { ModuleAnalysis }
    compiler.driver.module_analysis --> compiler.frontend.kernel_host | project.kernel_snapshot { ModuleAnalysis, analyze_module }
    compiler.driver.module_analysis --> project.compiler_host.ProjectHost.native_analyze { analyze_module }
    type compiler.driver.module_analysis --> compiler.frontend.host | project.compiler_host { ModuleAnalysis }
    compiler.driver.na_coverage --> project.compiler_host.ProjectHost.record_native_coverage { na_coverage_record }
    compiler.driver.native_iface --> compiler.driver.jir.native_deps_section { native_unit_ref }
    compiler.driver.native_iface --> compiler.driver.jir.parse_native_dep_rows { resolve_native_unit_ref }
    compiler.driver.nativecache --> project.compiler_host.ProjectHost.native_units_for { NativeUnitRegistry }
    type compiler.driver.nativecache --> compiler.frontend.host | compiler.frontend.kernel_host | project.compiler_host { NativeUnitRegistry }
    compiler.driver.pass_driver --> compiler.driver.program.JacProgram.load_dependency_module { run_pass }
    compiler.driver.pass_driver --> compiler.driver.session_compile.compile_in_session { compile_progress }
    compiler.driver.pipeline_runner --> cli.commands.analysis._check_file_job | compiler.driver.application._prepare | dist.precompile_bytecode._application_sources { compile_application }
    compiler.driver.pipeline_runner --> client.compiler.ViteCompiler._compile_wasm_module | compiler.backends.native.wasm_build.compile_to_wasm { build_wasm }
    compiler.driver.pipeline_runner --> client.route_scanner.resolve_route_exports | compiler.driver.application.prepare_route_metadata { route_exports }
    compiler.driver.pipeline_types --> compiler.driver.module_analysis { AnalysisFact }
    compiler.driver.program --> compiler.driver.module_analysis | compiler.driver.session_compile | compiler.frontend.kernel_analyze | compiler.frontend.kernel_host | compiler.tests.test_module_exports | compiler.tools.cfg_dot.cfg_dot_from_file | compiler.tools.jac_formatter_pass.unparse_module | dist.precompile_bytecode.prebuild_native_closure | dist.seal | project.kernel_check | project.kernel_snapshot { JacProgram }
    type compiler.driver.program --> compiler.backends.native.kernel_resolve | compiler.backends.native.kernel_stage0 | compiler.boundary_audit | compiler.driver.ifacecache | compiler.frontend.host | compiler.passes.context | compiler.passes.execution | compiler.passes.layout_pass | compiler.placement.placement | compiler.placement.placement_export | compiler.placement.placement_facts | compiler.placement.placement_pins | compiler.placement.placement_work | project.compiler_host { JacProgram }
    compiler.driver.session_compile --> compiler.driver.compiler { CompileFrame, SessionContext, SessionHooks }
    compiler.driver.session_compile --> compiler.driver.compiler.JacCompiler.compile { compile_in_session }
    compiler.driver.session_compile --> compiler.frontend.kernel_host { SessionHooks, compile_in_session }
    compiler.driver.session_compile --> project.kernel_snapshot { CompileFrame, SessionContext, SessionHooks, compile_in_session }
    compiler.driver.setup_progress --> compiler.driver.compiler { setup_progress }
    compiler.driver.source_failures --> compiler.driver.toolchain | project.compiler_host.ProjectHost.load_modules { fail_loud_on_compiler_source }
    compiler.driver.source_failures --> project.compiler_host.ProjectHost.import_in_flight { module_import_in_flight }
    compiler.driver.toolchain --> dist.precompile_bytecode.seal_native | project.compiler_host.ProjectHost.native_pipeline_available { native_pipeline_available }
    compiler.driver.wiring --> compiler.frontend.kernel_host.KernelHost.wiring_file | project.compiler_host.ProjectHost.wiring_file { arch_file_for, is_arch_file }
    compiler.driver.wiring --> project.compiler_host.ProjectHost.session { wiring_scope }
    compiler.driver.pipeline as pipeline --> scale.tests.apps.test_fleet_from_apps;
    compiler.driver.wiring --> compiler.frontend.kernel_host.KernelHost.place_wired_imports | project.compiler_host.ProjectHost.place_wired_imports { dedupe_generated_imports }
    compiler.driver.wiring --> compiler.tools.jac_auto_lint_pass.JacAutoLintPass._strip_wired_imports { is_kernel_abi_contract, is_native_stdlib_source }
    compiler.driver.application --> cli.commands.execution._load_executable { prepare_application }
    compiler.driver.application --> compiler.driver.build_services.CompilerBuildServices.prepare_dynamic_module { prepare_dynamic_module }
    compiler.driver.bccache --> compiler.driver.nativecache._module_files_and_imports { discover_annex_files }
    compiler.driver.bccache --> testing.cl_test_runner.module_entry_for { discover_base_file }
    compiler.driver.boundary_classify --> compiler.driver.program.JacProgram.stamp_native_import_facts { import_bound_names, python_side_name_refs }
    compiler.driver.compilation_context --> compiler.driver.application._prepare_revision { cache_scope, program_for }
    compiler.driver.compilation_context --> compiler.driver.jir._module_projection { active_options }
    compiler.driver.compilation_context --> packages.api.package_surface { compilation_scope }
    compiler.driver.compile_options --> compiler.driver.nativecache.NativeUnitRegistry._miss { env_na_debug }
    compiler.driver.compile_options --> compiler.driver.nativecache.NativeUnitRegistry.record_module { env_na_debug }
    compiler.driver.compile_options --> packages.api.package_surface { CompileOptions }
    compiler.driver.jir --> compiler.backends.native.link_plan.LinkPlan.plan_digest { native_producer_digest }
    compiler.driver.jir --> compiler.backends.native.link_plan._write_sidecar { native_producer_digest }
    compiler.driver.jir --> compiler.driver.application._capture_input { ct_dep_digest }
    compiler.driver.jir --> compiler.driver.application._prepare_revision { cache_mode, ct_dep_digest }
    compiler.driver.jir --> compiler.driver.compiler { FLAG_CARRIED, carried_module_bytecode }
    compiler.driver.jir --> compiler.driver.compiler.JacCompiler._get_bytecode { SEC_CTDEPS as _CARRY_CTDEPS }
    compiler.driver.jir --> compiler.driver.ifacecache { module_ct_deps_section }
    compiler.driver.jir --> compiler.driver.nativecache { PRECOMPILE_SENTINEL, carried_native_sections, compute_content_sha256, module_cache_invalid_reason, module_ct_deps_section, native_producer_digest, stale_ct_dep_rows, write_module_cache }
    compiler.driver.jir --> compiler.driver.nativecache.NativeUnitRegistry.emit_objects { write_module_cache }
    compiler.driver.jir --> dist.precompile_bytecode { require_exact_compiler_products }
    compiler.driver.jir --> packages.artifact.package_manifest | packages.resolve.resolve_graph { jaclang_version }
    compiler.driver.jir --> packages.resolve.running_jac_version { jaclang_version }
    compiler.driver.pass_driver --> compiler.driver.application._prepare { compile_progress }
    compiler.driver.pipeline_runner --> compiler.driver.application._prepare_revision { compile_application }
    compiler.driver.program --> compiler.driver.jir._definition_texts | compiler.driver.nativecache._module_files_and_imports | packages.api.package_surface { JacProgram }
    compiler.driver.source_failures --> compiler.driver.application._prepare_revision { bootstrap_tier_failure_details, module_scoped_failure_details }
    compiler.driver.wiring --> compiler.passes.package_boundary_pass { local_module_name }
    compiler.driver.bccache --> compiler.driver.application._stamp { LISTING_SETTLE_NS }
    compiler.driver.bccache --> project.kernel_snapshot.session_inputs { host_layout_tables }
    compiler.driver.compilation_context --> compiler.driver.compiler.JacCompiler.last_client_artifact { compilation_scope, owner_scope_options }
    compiler.driver.compilation_context --> compiler.driver.unit_products.dependency_span_rows { program_for }
    compiler.driver.compile_options --> compiler.backends.native.link_plan.plan_objects { env_symmap_requested }
    compiler.driver.compile_options --> compiler.driver.module_compile { CompileOptions }
    compiler.driver.compile_options --> project.kernel_compile { CompileOptions }
    compiler.driver.compiler --> project.compiler_host.ProjectHost.client_pulls { cached_client_pulls }
    compiler.driver.jir --> client.client_bundle.ClientBundleBuilder._signature { ct_dep_digest }
    compiler.driver.jir --> compiler.driver.application._stamp { compute_content_sha256 }
    compiler.driver.jir --> compiler.driver.compiler { SEC_CTDEPS, ct_deps_section, seed_definition_texts }
    compiler.driver.jir --> project.compiler_host.ProjectHost.in_compiler_tree { is_compiler_tree_path }
    compiler.driver.jir --> project.kernel_snapshot.compiled_already { get_module_cache_path, is_module_cache_valid }
    compiler.driver.module_analysis --> compiler.driver.module_compile { ModuleAnalysis, analyze_module }
    compiler.driver.module_compile --> compiler.driver.compiler { compile_module }
    compiler.driver.module_compile --> compiler.frontend.kernel_host { compile_task }
    compiler.driver.pass_driver --> compiler.driver.compiler.JacCompiler._adopt_kernel_compile { compile_progress }
    compiler.driver.pass_driver --> compiler.driver.module_compile.report_missing_native_ir { deliver_alerts }
    compiler.driver.pipeline --> compiler.driver.application._tree_source { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.driver.module_compile { CompilationProduct }
    compiler.driver.program --> compiler.driver.module_compile { JacProgram }
    compiler.driver.program --> compiler.driver.unit_products { JacProgram }
    compiler.driver.program --> project.kernel_compile { JacProgram }
    compiler.driver.session_compile --> compiler.driver.module_compile { SessionHooks }
    compiler.driver.source_failures --> project.compiler_host.ProjectHost.schedule_import_failed { fail_loud_on_compiler_source }
    compiler.driver.unit_products --> compiler.boundary_audit.boundary_audit { interop_record }
    compiler.driver.unit_products --> compiler.driver.application._import_edges_of { DEF_DEP_SEP as EDGE_SEP }
    compiler.driver.unit_products --> compiler.driver.application._tree_source { import_edge_rows }
    compiler.driver.unit_products --> compiler.driver.application._unit_source { interop_manifest_of, manifest_from_record }
    compiler.driver.unit_products --> compiler.driver.compiler { UnitProducts, client_artifact_from_json, client_artifact_json, client_artifact_of, definition_deps, interop_manifest_of, interop_record, placement_record, unit_products }
    compiler.driver.unit_products --> compiler.driver.ifacecache.IfaceRegistry._persist_in_context { interop_record }
    compiler.driver.unit_products --> compiler.driver.ifacecache.IfaceRegistry.client_boundary_facts { interop_manifest_of }
    compiler.driver.unit_products --> compiler.driver.jir._definition_texts { definition_span_rows }
    compiler.driver.unit_products --> compiler.driver.jir._texts_of_spans { DEF_DEP_SEP }
    compiler.driver.unit_products --> compiler.driver.jir.seed_definition_texts { DEF_DEP_SEP }
    compiler.driver.unit_products --> compiler.frontend.kernel_analyze { UnitProducts, products_from_record, products_record }
    compiler.driver.unit_products --> compiler.frontend.kernel_host { UnitProducts, unit_interface, unit_products }
    compiler.driver.unit_products --> project.kernel_compile { UnitProducts }
    compiler.driver.wiring --> compiler.driver.jir.stored_wiring_digest { arch_file_for, import_prefix_for, is_arch_file, wiring_digest_for }
    compiler.driver.bccache --> cli.commands.analysis._unit_weight { discover_annex_files }
    compiler.driver.boundary_classify --> compiler.driver.program.JacProgram.stamp_native_import_facts { clib_decl_type_names }
    compiler.driver.boundary_classify --> compiler.passes.placement_pass.PlacementPass._run_undecided { _stamp_context_element }
    compiler.driver.boundary_classify --> compiler.passes.placement_pass.uncrossable_native { _stamp_context_element }
    compiler.driver.boundary_classify --> compiler.placement.placement.native_blocker_scan { ability_delegates_to_model }
    compiler.driver.boundary_classify --> compiler.placement.placement_facts.settle_server { _stamp_context_element }
    compiler.driver.boundary_classify --> compiler.placement.placement_solver.dependency_summary { hub_module_for_path }
    compiler.driver.compilation_context --> compiler.driver.jir._memoized { active_options }
    compiler.driver.compilation_context --> compiler.types.type_evaluator.TypeEvaluator._in_flight_module { program_for }
    compiler.driver.compile_options --> compiler.backends.native.llvm.ir.types { env_typed_pointers_enabled }
    compiler.driver.context_passes --> compiler.driver.pipeline { NativeImportFactsPass }
    compiler.driver.ifacecache --> cli.commands.analysis.check { prime_iface_codec }
    compiler.driver.jir --> client.jac_client_compiler.JacClientCompiler.emit_dependencies { compute_content_sha256 }
    compiler.driver.jir --> client.targets.desktop._dev_launch._dev_roots_from_env { dev_source }
    compiler.driver.jir --> compiler.backends.native.kernel_resolve.KernelArtifact.build { require_exact_compiler_products }
    compiler.driver.jir --> compiler.backends.native.kernel_resolve._inspect { sidecar_unit_paths }
    compiler.driver.jir --> compiler.backends.native.kernel_resolve.unit_drift { native_producer_digest, running_compiler_digest, unit_source_digest }
    compiler.driver.jir --> compiler.driver.application._prepare { begin_prepare_memo, end_prepare_memo }
    compiler.driver.jir --> dist.precompiled.bundle_misses { jir_cacheable_source_path, precompiled_jir_matches_source }
    compiler.driver.jir --> project.compiler_host.ProjectHost.save_native_debug_ir { get_native_debug_dir }
    compiler.driver.module_analysis --> compiler.driver.module_compile { PlanStep, run_plan }
    compiler.driver.na_coverage --> cli.commands.analysis._check_file_job { na_coverage_snapshot }
    compiler.driver.na_coverage --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._place_unit_python { na_coverage_seam }
    compiler.driver.native_iface --> compiler.driver.nativecache.NativeUnitRegistry.adopt_lowered { native_layout_from_dict }
    compiler.driver.native_iface --> compiler.driver.unit_products.native_products { native_layout_to_dict }
    type compiler.driver.native_iface --> compiler.frontend.host | project.compiler_host { NativeIface }
    compiler.driver.native_iface --> compiler.frontend.kernel_host { NativeIface }
    compiler.driver.pass_driver --> compiler.driver.pipeline.run_utility { run_pass }
    compiler.driver.pipeline --> cli.commands.analysis.grammar { run_utility }
    compiler.driver.pipeline --> cli.commands.transform.py2jac { run_utility }
    compiler.driver.pipeline --> compiler.backends.es.client_kernel_cache._lower { require }
    compiler.driver.pipeline --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._ensure_dep_inference { require }
    compiler.driver.pipeline --> compiler.driver.application._tree_source { require }
    compiler.driver.pipeline --> compiler.driver.application_edges.application_edges { require }
    compiler.driver.pipeline --> compiler.driver.compiler.JacCompiler.assemble_native { require }
    compiler.driver.pipeline --> compiler.driver.compiler.JacCompiler.assemble_python { require }
    compiler.driver.pipeline --> compiler.driver.compiler.JacCompiler.ensure_client_codegen { require }
    compiler.driver.pipeline --> compiler.driver.compiler.JacCompiler.jac_file_formatter { require }
    compiler.driver.pipeline --> compiler.driver.compiler.JacCompiler.jac_file_linter { require }
    compiler.driver.pipeline --> compiler.driver.compiler.JacCompiler.jac_str_formatter { require }
    compiler.driver.pipeline --> compiler.driver.ifacecache.IfaceRegistry._ensure_flow_graph { require }
    compiler.driver.pipeline --> compiler.driver.ifacecache.IfaceRegistry._ensure_in_context { require }
    compiler.driver.pipeline --> compiler.driver.ifacecache.IfaceRegistry._prepare { product_facts }
    compiler.driver.pipeline --> compiler.driver.module_analysis.ModuleAnalysis.ready { product_ready }
    compiler.driver.pipeline --> compiler.driver.module_analysis.ModuleAnalysis.require { require }
    compiler.driver.pipeline --> compiler.driver.module_compile { product_passes, unavailable }
    compiler.driver.pipeline --> compiler.driver.nativecache.NativeBuildSession._finish { require }
    compiler.driver.pipeline --> compiler.driver.nativecache.NativeBuildSession.lower { invalidate, require }
    compiler.driver.pipeline --> compiler.driver.source_failures.bootstrap_tier_failure_details { tier_reason }
    compiler.driver.pipeline --> compiler.driver.toolchain { schedule_loading }
    compiler.driver.pipeline --> compiler.frontend.kernel_host.KernelHost.lower_dependency { product_ready, require }
    compiler.driver.pipeline --> compiler.jc_unit { early_passes }
    compiler.driver.pipeline --> compiler.passes.layout_pass.get_layout_registry { require }
    compiler.driver.pipeline --> compiler.placement.placement_solver.invalidate_importers_es { invalidate }
    compiler.driver.pipeline --> compiler.placement.placement_solver.solve_module_placement._invalidate_stale_codegen { invalidate }
    compiler.driver.pipeline --> compiler.tests.test_module_exports { run_utility }
    compiler.driver.pipeline --> compiler.tests.test_pipeline_products { _LOADING, product_facts, require }
    compiler.driver.pipeline --> compiler.tools.cfg_dot.cfg_dot_from_file { run_utility }
    compiler.driver.pipeline --> compiler.tools.jac_formatter_pass.format_module { run_utility }
    compiler.driver.pipeline --> compiler.tools.jac_formatter_pass.unparse_module { run_utility }
    compiler.driver.pipeline --> compiler.tools.lang_tools { require }
    compiler.driver.pipeline --> compiler.tools.lang_tools.AstTool.ir { run_utility }
    compiler.driver.pipeline --> dist.publish.npm_sources._compile_module { require }
    compiler.driver.pipeline --> project.compiler_host.ProjectHost.parse_python { run_utility }
    compiler.driver.pipeline_types --> cli.commands.analysis.grammar { CompilationProduct }
    compiler.driver.pipeline_types --> cli.commands.transform.py2jac { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.backends.es.esast_gen_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.backends.native.na_compile_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.backends.native.na_ir_gen_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.backends.py.jcir_bc_gen_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.backends.py.jcir_gen_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.driver.compiler { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.driver.context_passes { PassContract }
    compiler.driver.pipeline_types --> compiler.driver.ifacecache.IfaceRegistry._ensure_flow_graph { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.driver.ifacecache.IfaceRegistry._ensure_in_context { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.driver.ifacecache.IfaceRegistry._prepare { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.driver.module_analysis { CompilationProduct, ProductRequest }
    compiler.driver.pipeline_types --> compiler.driver.module_compile { ProductRequest }
    compiler.driver.pipeline_types --> compiler.driver.nativecache.NativeBuildSession._finish { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.driver.pipeline { ImportFallback, ProductRequest }
    compiler.driver.pipeline_types --> compiler.driver.source_failures.bootstrap_tier_failure_details { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.frontend.kernel_host.KernelHost.lower_dependency { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.passes.access_check_pass { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.passes.ast_validation_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.passes.boundary_analysis_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.passes.capability_check_pass { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.passes.cfg_build_pass { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.passes.comptime_resolve_pass { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.passes.context { PassContract }
    compiler.driver.pipeline_types --> compiler.passes.decl_impl_match_pass { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.passes.endpoint_effect_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.passes.freeze_structure_pass { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.passes.graph_lowering_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.passes.import_wiring_pass { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.passes.jsx_intrinsic_guard_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.passes.layout_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.passes.mtir_gen_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.passes.ownership_check_pass { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.passes.package_boundary_pass { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.passes.placement_pass { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.passes.pyast_load_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.passes.rc_facts_pass { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.passes.region_infer_pass { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.passes.sem_def_match_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.passes.semantic_analysis_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.passes.static_analysis_pass { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.passes.sym_tab_build_pass { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.passes.type_checker_pass { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.passes.variant_agreement_pass { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.placement.placement_solver { AnalysisFact, PassContract }
    compiler.driver.pipeline_types --> compiler.placement.placement_solver.invalidate_importers_es { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.placement.placement_solver.solve_module_placement._invalidate_stale_codegen { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.tests.test_module_exports { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.tests.test_pipeline_products { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.tools.cfg_dot { PassContract }
    compiler.driver.pipeline_types --> compiler.tools.cfg_dot.cfg_dot_from_file { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.tools.comment_attach_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.tools.doc_ir_gen_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.tools.grammar_extract_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.tools.jac_auto_lint_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.tools.jac_formatter_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.tools.jac_formatter_pass.format_module { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.tools.jac_formatter_pass.unparse_module { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.tools.lang_tools.AstTool.ir { CompilationProduct }
    compiler.driver.pipeline_types --> compiler.tools.normalize_pass { PassContract }
    compiler.driver.pipeline_types --> compiler.tools.unparse_pass { PassContract }
    compiler.driver.pipeline_types --> project.compiler_host.ProjectHost.parse_python { CompilationProduct }
    compiler.driver.program --> compiler.backends.native.kernel_stage0.link_kernel { JacProgram }
    type compiler.driver.program --> compiler.capability_notes { JacProgram }
    type compiler.driver.program --> compiler.native_bindings { JacProgram }
    type compiler.driver.program --> compiler.passes.placement_pass { JacProgram }
    compiler.driver.program --> dist.publish.builder._backend_source { JacProgram as JacProgramRt }
    type compiler.driver.session_compile --> compiler.driver.module_analysis { SessionHooks }
    compiler.driver.session_compile --> compiler.passes.placement_pass.settle_native_module { drop_native_bindings }
    compiler.driver.toolchain --> compiler.backends.native.kernel_resolve.KernelArtifact.unavailable_reason { native_pipeline_available }
    compiler.driver.jir --> compiler.driver.application._reusable_interfaces { compute_module_key }
    compiler.driver.jir --> compiler.driver.application._unit_row { compute_module_key }
    compiler.driver.unit_products --> compiler.driver.application._row_unit { UnitProducts }
    compiler.frontend.host --> project.compiler_host.ProjectHost.native_fact { HOST_FACT_GIT_IGNORED, HOST_FACT_SEP, HOST_FACT_STDLIB_MODULES }
    compiler.frontend.codeinfo --> cli.check_report.print_native_coverage { effective_default_codespace, native_display_text }
    compiler.frontend.codeinfo --> cli.commands.execution._exec_file { get_effective_default_codespace_override, set_effective_default_codespace }
    compiler.frontend.codeinfo --> cli.commands.execution.serve { set_effective_default_codespace }
    type compiler.frontend.codeinfo --> client.client_bundle { ClientArtifact, ClientManifest }
    type compiler.frontend.codeinfo --> client.compiler { ClientArtifact, ClientManifest }
    compiler.frontend.codeinfo --> client.compiler.ViteCompiler._compile_wasm_module { native_wasm_stem }
    type compiler.frontend.codeinfo --> client.jac_client_compiler { ClientArtifact, ClientManifest }
    type compiler.frontend.codeinfo --> client.jac_to_js { ClientArtifact, ClientManifest }
    compiler.frontend.codeinfo --> client.vite_client_bundle { ClientArtifact }
    compiler.frontend.codeinfo --> compiler.backends.es.client_kernel_cache._es_backend_fingerprint { jaclang_pkg_root }
    compiler.frontend.codeinfo --> compiler.backends.es.client_kernel_cache._unit_source_path { kernel_unit_path }
    compiler.frontend.codeinfo --> compiler.backends.es.esast_gen_pass { BoundaryTypeInfo, ClientManifest }
    compiler.frontend.codeinfo --> compiler.backends.es.esast_gen_pass.EsastGenPass._build_spawn_runtime_call { endpoint_key }
    compiler.frontend.codeinfo --> compiler.backends.es.esast_gen_pass.EsastGenPass._generate_na_import_binding { native_wasm_stem }
    compiler.frontend.codeinfo --> compiler.backends.es.esast_gen_pass.EsastGenPass._generate_sv_import_stubs { endpoint_key }
    compiler.frontend.codeinfo --> compiler.backends.es.esast_gen_pass.EsastGenPass._try_lower_server_rpc_call { endpoint_key }
    compiler.frontend.codeinfo --> compiler.backends.es.esast_gen_pass.EsastGenPass.prepare { ClientManifest }
    compiler.frontend.codeinfo --> compiler.backends.native.kernel_resolve.source_tree_kernel_path { jaclang_pkg_root }
    type compiler.frontend.codeinfo --> compiler.backends.native.link_glue { InteropBinding }
    compiler.frontend.codeinfo --> compiler.backends.native.link_glue.inject_heap_accounting { HDR_TOTAL }
    compiler.frontend.codeinfo --> compiler.backends.native.link_plan { kernel_unit_path }
    type compiler.frontend.codeinfo --> compiler.backends.native.link_plan { InteropBinding }
    compiler.frontend.codeinfo --> compiler.backends.native.link_plan._build_link_plan { is_kernel_unit_path }
    compiler.frontend.codeinfo --> compiler.backends.native.link_plan._write_sidecar { native_unit_identity }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass { HDR_ALLOC_ID_OFF, HDR_DTOR_OFF, HDR_MAGIC, HDR_MAGIC_SHIFT_BASE, HDR_RC_OFF, HDR_TAG_OFF, HDR_TOTAL, JACSTR_DESC_FIELDS, RC_SENTINEL, STR_LEN_TAG_BIT, STR_LEN_TAG_SHIFT, str_len_tag }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass.__post_init__ { native_unit_prefix }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._arch_display { native_arch_display }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_call { resolve_native_module }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_entry { native_entry_name, native_runtime_probe_name }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_test { native_test_symbol }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._emit_class_display_fn { NATIVE_ARCH_SCOPE_SEP }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._emit_glob_init_func { native_glob_init_name }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._emit_jacval_slot_drop_fn { native_safe_sym }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._ensure_fmt_kernel { FMT_KERNEL_REL, kernel_unit_path }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._eq_fn_new { native_safe_sym }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._export_native_iface { native_glob_init_name, native_module_key, native_unit_spelling }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._export_native_layout { NativeEnumLayout, NativeFieldInfo, NativeFuncLayout, NativeModuleLayout, NativeStructLayout, NativeTestLayout, NativeTupleLayout }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._find_source_ability { resolve_native_module }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._forward_declare_imported_ability { native_def_symbol }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._is_kernel_unit { is_kernel_unit_path }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._native_module_call_target { NATIVE_STDLIB_EXTENSIONS }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._opaque_field_if_unlowerable { native_display_text }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._osp_kernel_init_fns { native_glob_init_name }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._prefix_of_path { native_unit_prefix }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._process_clib_imports { is_bundled_native_module, resolve_native_module }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._pyb_base_of { NATIVE_ERASED_BASES }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._register_entry_globals { native_def_symbol }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._register_imported_struct_types { is_bundled_native_module, native_unit_compile_active as _typed_nuc, resolve_native_module }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._register_osp_kernel_module { OSP_GRAPH_REL, OSP_KERNEL_REL, kernel_unit_path }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._register_region_kernel { REGION_KERNEL_REL, kernel_unit_path }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._repr_dict_fn { native_safe_sym }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._repr_leaf_fn { native_safe_sym }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._repr_list_fn { native_safe_sym }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._repr_obj_fn { native_safe_sym }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._repr_set_fn { native_safe_sym }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._repr_str_fn { native_safe_sym }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._repr_tuple_fn { native_safe_sym }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._skip_is_other_module { resolve_native_module }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._symbol_for { native_def_symbol, native_symbol_name, native_unit_identity, native_unit_spelling }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._vtable_symbol { native_symbol_name, native_unit_spelling }
    compiler.frontend.codeinfo --> compiler.backends.native.region_abi._region_layout_facts { HDR_ALLOC_ID_OFF, HDR_DTOR_OFF, HDR_MAGIC, HDR_MAGIC_SHIFT_BASE, HDR_RC_OFF, HDR_TAG_OFF, HDR_TOTAL, RC_SENTINEL }
    compiler.frontend.codeinfo --> compiler.backends.py.jcir_gen_pass { BoundaryTypeInfo, InteropBinding }
    compiler.frontend.codeinfo --> compiler.backends.py.jcir_gen_pass.JcirGenPass._class_ref { module_dotted_name }
    compiler.frontend.codeinfo --> compiler.backends.py.jcir_gen_pass.JcirGenPass._gen_native_interop_stubs { native_def_symbol, native_symbol_name, native_unit_prefix }
    compiler.frontend.codeinfo --> compiler.backends.py.jcir_gen_pass.JcirGenPass._materialize { module_dotted_name }
    compiler.frontend.codeinfo --> compiler.backends.py.jcir_gen_pass.JcirGenPass._native_test_shim_stmts { native_test_symbol, native_unit_prefix }
    compiler.frontend.codeinfo --> compiler.backends.py.jcir_gen_pass.JcirGenPass._sv_endpoint_effects { endpoint_key }
    compiler.frontend.codeinfo --> compiler.backends.py.jcir_gen_pass.JcirGenPass.exit_archetype { endpoint_key }
    compiler.frontend.codeinfo --> compiler.driver.application.prepare_application { get_effective_default_codespace_override, set_effective_default_codespace }
    compiler.frontend.codeinfo --> compiler.driver.boundary_classify._default_codespace_for { effective_default_codespace }
    compiler.frontend.codeinfo --> compiler.driver.boundary_classify.bridgeable_import_target { is_shared_runtime_module }
    compiler.frontend.codeinfo --> compiler.driver.boundary_classify.import_binds_client_native { InteropContext, InteropManifest }
    compiler.frontend.codeinfo --> compiler.driver.build_services.CompilerBuildServices.prepare_application { set_effective_default_codespace }
    type compiler.frontend.codeinfo --> compiler.driver.client_graph { ClientArtifact }
    compiler.frontend.codeinfo --> compiler.driver.compile_options.CompileOptions.__post_init__ { effective_native_target }
    compiler.frontend.codeinfo --> compiler.driver.compile_options.CompileOptions.native_required_for { module_dotted_name }
    compiler.frontend.codeinfo --> compiler.driver.compile_options.pop_native_target { _native_target_ctx }
    compiler.frontend.codeinfo --> compiler.driver.compile_options.push_native_target { set_native_target_override }
    type compiler.frontend.codeinfo --> compiler.driver.compiler { CodeGenTarget, NativeModuleLayout }
    compiler.frontend.codeinfo --> compiler.driver.compiler.JacCompiler._cached_client_artifact { ClientArtifact }
    compiler.frontend.codeinfo --> compiler.driver.compiler.JacCompiler._check_native_abi { NATIVE_ABI_VERSION }
    compiler.frontend.codeinfo --> compiler.driver.compiler.JacCompiler._load_native_from_cache { CodeGenTarget }
    compiler.frontend.codeinfo --> compiler.driver.compiler.JacCompiler._restore_sections { ClientArtifact }
    compiler.frontend.codeinfo --> compiler.driver.ifacecache.IfaceRegistry.client_boundary_facts { CodeGenTarget }
    compiler.frontend.codeinfo --> compiler.driver.jir._analysis_fingerprint_for { effective_native_target }
    compiler.frontend.codeinfo --> compiler.driver.jir._module_codespace_mode { effective_default_codespace }
    compiler.frontend.codeinfo --> compiler.driver.native_iface { NativeModuleLayout }
    type compiler.frontend.codeinfo --> compiler.driver.nativecache { CodeGenTarget }
    compiler.frontend.codeinfo --> compiler.driver.nativecache.NativeBuildSession.lower { get_effective_default_codespace_override, reset_native_unit_compile, set_effective_default_codespace, set_native_unit_compile }
    compiler.frontend.codeinfo --> compiler.driver.nativecache.NativeUnitRegistry._source_key { get_effective_default_codespace_override, set_effective_default_codespace }
    compiler.frontend.codeinfo --> compiler.driver.nativecache.NativeUnitRegistry._stash_products { CodeGenTarget }
    type compiler.frontend.codeinfo --> compiler.driver.progstate { ClientArtifact }
    compiler.frontend.codeinfo --> compiler.driver.selfhost.SelfHostCache.evict_unit { CodeGenTarget }
    compiler.frontend.codeinfo --> compiler.driver.selfhost.SelfHostCache.resolve { is_native_by_location, is_shared_runtime_module, native_unit_compile_active }
    type compiler.frontend.codeinfo --> compiler.frontend.unitree { CodeGenTarget }
    compiler.frontend.codeinfo --> compiler.frontend.unitree.ModulePath.native_bundled_path { NATIVE_STDLIB_EXTENSIONS, is_bundled_native_module, resolve_native_module }
    compiler.frontend.codeinfo --> compiler.frontend.unitree.UniNode.gen.getter { CodeGenTarget as _CGT }
    compiler.frontend.codeinfo --> compiler.native_scope.scope_allows_inferred_path { native_unit_compile_active, native_unit_identity }
    compiler.frontend.codeinfo --> compiler.passes.boundary_analysis_pass { BoundaryTypeInfo, InteropBinding, InteropContext }
    compiler.frontend.codeinfo --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._collect_boundary_type { endpoint_key }
    compiler.frontend.codeinfo --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._register_na_client_import { native_wasm_stem }
    compiler.frontend.codeinfo --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass.finish { endpoint_key }
    compiler.frontend.codeinfo --> compiler.passes.capability_check_pass { NATIVE_SUPPORTED_STDLIB, is_native_by_location }
    compiler.frontend.codeinfo --> compiler.passes.capability_check_pass.base_expr_is_erased { NATIVE_ERASED_BASES }
    compiler.frontend.codeinfo --> compiler.passes.capability_check_pass.classify_native_import { native_erased_import_names }
    compiler.frontend.codeinfo --> compiler.passes.capability_check_pass.native_capability_violations { bundled_native_module_names, is_bundled_native_module, resolve_native_module }
    compiler.frontend.codeinfo --> compiler.passes.endpoint_effect_pass.EndpointEffectPass._classify { endpoint_descriptor }
    compiler.frontend.codeinfo --> compiler.passes.endpoint_effect_pass.EndpointEffectPass.enter_ability { endpoint_key }
    compiler.frontend.codeinfo --> compiler.passes.endpoint_effect_pass.EndpointEffectPass.enter_archetype { endpoint_key }
    compiler.frontend.codeinfo --> compiler.passes.layout_pass.is_erased_base_name { NATIVE_ERASED_BASES }
    compiler.frontend.codeinfo --> compiler.placement.placement._erased_only_import { native_erased_import_names }
    compiler.frontend.codeinfo --> compiler.placement.placement_facts.native_unit { is_kernel_unit_path, native_unit_compile_active }
    compiler.frontend.codeinfo --> compiler.placement.placement_solver._native_deps_ok { native_unit_compile_active }
    compiler.frontend.codeinfo --> compiler.tests.xbackend_equiv { JAC_ENTRY_SYMBOL, native_symbol_name, native_unit_prefix }
    compiler.frontend.codeinfo --> compiler.tests.xbackend_equiv.run_js_module_fixture { ClientArtifact, ClientManifest }
    compiler.frontend.codeinfo --> compiler.tools.comment_attach_pass { NodeComments }
    compiler.frontend.codeinfo --> compiler.types.ct_eval { module_dotted_name }
    compiler.frontend.codeinfo --> compiler.types.types.ClassDetailsShared.same_class { bundled_stdlib_module_of }
    compiler.frontend.codeinfo --> dist.source.client.write_client { native_wasm_stem }
    compiler.frontend.codeinfo --> lsp.server.utils { CodeLocInfo }
    compiler.frontend.codeinfo --> runtime.portability { NATIVE_SUPPORTED_STDLIB, is_bundled_native_module }
    compiler.frontend.const_fold --> compiler.backends.native.na_ir_gen_pass { fold_const }
    compiler.frontend.const_fold --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_const_expr { fold_const }
    compiler.frontend.const_fold --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._folded_ord { fold_const }
    compiler.frontend.const_fold --> compiler.passes.layout_pass { fold_const }
    compiler.frontend.const_fold --> compiler.types.enum_utils { fold_const }
    compiler.frontend.const_fold --> compiler.types.operations.get_pow_result_type { fold_const }
    compiler.frontend.constant --> cli.commands.fix._priv_top_decls { SymbolAccess }
    compiler.frontend.constant --> compiler.backends.es.esast_gen_pass { CodeContext, SymbolType, Tokens as Tok }
    compiler.frontend.constant --> compiler.backends.es.framework_backend.FrameworkBackend._get_setter_name { client_state_setter_name }
    compiler.frontend.constant --> compiler.backends.es.free_ident_audit { BROWSER_SEED_GLOBALS }
    compiler.frontend.constant --> compiler.backends.es.jac_runtime_js._build_types_runtime_js { TOKEN_MAP }
    compiler.frontend.constant --> compiler.backends.native.foreign { is_borrow_kind }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass { CodeContext, OwnershipKind, SymbolAccess, Tokens as Tok }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._clib_place_ptr { is_borrow_kind }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_assignment { OwnershipKind }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_unary { OwnershipKind, is_borrow_kind }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._ct_fold { ExprCtx }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._flow_future_licensed { Tokens as Tok }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._hl_view_base_licensed { OwnershipKind }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._nogc_borrow_local_assign { is_borrow_kind }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._nogc_consume_assigned_local { OwnershipKind, is_borrow_kind }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._predeclare_nested_siblings { SymbolType }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._try_flow_for_parallel { Tokens as Tok }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._try_flow_future { Tokens as Tok }
    compiler.frontend.constant --> compiler.backends.native.primitives_native { Tokens as Tok }
    compiler.frontend.constant --> compiler.backends.py.jcir_gen_pass { CodeContext, OwnershipKind, SymbolStorage, Tokens as Tok, is_borrow_kind }
    compiler.frontend.constant --> compiler.backends.py.jcir_gen_pass.JcirGenPass._gen_native_interop_stubs { Tokens as _NsTok }
    compiler.frontend.constant --> compiler.c_interop.foreign_read_is_place { is_borrow_kind }
    compiler.frontend.constant --> compiler.driver.boundary_classify { CodeContext, SymbolAccess, Tokens as Tok }
    compiler.frontend.constant --> compiler.driver.boundary_classify.module_own_native_anchor { OwnershipKind }
    compiler.frontend.constant --> compiler.driver.compiler { CodeContext }
    compiler.frontend.constant --> compiler.driver.ifacecache.IfaceRegistry._client_edges { CodeContext }
    compiler.frontend.constant --> compiler.driver.wiring { Tokens as Tok }
    compiler.frontend.constant --> compiler.expr_keys { Tokens as Tok }
    compiler.frontend.constant --> compiler.expr_keys.type_tag_borrows { is_borrow_kind }
    compiler.frontend.constant --> compiler.frontend.codeinfo { NATIVE_ERASED_ANNOTATIONS, NATIVE_ERASED_TYPE_MARKERS, TYPE_PARAM_CONSTRUCTORS }
    compiler.frontend.constant --> compiler.frontend.helpers.evaluate_version_condition { Tokens as Tok }
    compiler.frontend.constant --> compiler.frontend.module_facts { CodeContext, NATIVE_ERASED_TYPE_MARKERS, TYPE_PARAM_CONSTRUCTORS }
    compiler.frontend.constant --> compiler.frontend.parser.parser { CodeContext, OwnershipKind, ParamKind, SymbolAccess, SymbolType, Tokens as Tok }
    compiler.frontend.constant --> compiler.frontend.unitree { BUILTIN_CALLABLE_NAMES, BindingKind, CodeContext, DELIM_MAP, DeleteTargetError, ExprCtx, ImmutabilityKind, JacSemTokenModifier as SemTokMod, JacSemTokenType as SemTokType, OwnershipKind, ParamKind, SymbolAccess, SymbolStorage, SymbolType, Tokens as Tok }
    compiler.frontend.constant --> compiler.frontend.unitree.UniNode.gen_token { TOKEN_MAP }
    compiler.frontend.constant --> compiler.jc_unit { CodeContext }
    compiler.frontend.constant --> compiler.passes.access_check_pass { SymbolAccess }
    compiler.frontend.constant --> compiler.passes.ast_validation_pass { CodeContext, DeleteTargetError, Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.boundary_analysis_pass { CodeContext, SymbolType, Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._get_context { CodeContext }
    compiler.frontend.constant --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._register_native_absorb { SymbolAccess }
    compiler.frontend.constant --> compiler.passes.capability_check_pass { SymbolType }
    compiler.frontend.constant --> compiler.passes.capability_check_pass.PortabilityWarnPass._check_js_globals { ExprCtx }
    compiler.frontend.constant --> compiler.passes.capability_check_pass.PortabilityWarnPass._check_js_keywords { ExprCtx }
    compiler.frontend.constant --> compiler.passes.capability_check_pass.native_capability_violations { CodeContext, ExprCtx, Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.cfg_build_pass.CFGBuildPass.exit_ctrl_stmt { Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.cfg_build_pass._bool_is_and { Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.endpoint_effect_pass { SymbolType, Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.graph_lowering_pass { Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.layout_pass { OwnershipKind, Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.mtir_gen_pass { Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.osp_analysis { CodeContext, Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.ownership_check_pass { OwnershipKind, SymbolStorage, Tokens as Tok, is_borrow_kind, is_mut_kind }
    compiler.frontend.constant --> compiler.passes.ownership_check_pass.OwnershipCheckPass._emit_flow_for_diagnostics { Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.ownership_check_pass.OwnershipCheckPass._emit_sendability_diagnostics { Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.ownership_check_pass.OwnershipCheckPass._flow_for_stmts { Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.ownership_check_pass.OwnershipCheckPass._flow_lend_joined { Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.ownership_check_pass.OwnershipCheckPass._flow_reduce_shape { Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.ownership_check_pass.OwnershipCheckPass._spawn_move_gen { Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.ownership_hints { OwnershipKind }
    compiler.frontend.constant --> compiler.passes.pyast_load_pass { RESERVED_IDENT_NAMES, Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.pyast_load_pass.PyastBuildPass.proc_aug_assign { TOKEN_MAP }
    compiler.frontend.constant --> compiler.passes.rc_facts_pass { ExprCtx, OwnershipKind, SymbolStorage, Tokens as Tok, is_borrow_kind }
    compiler.frontend.constant --> compiler.passes.rc_facts_pass.RcFactsPass._asn_makes_region_handle { OwnershipKind }
    compiler.frontend.constant --> compiler.passes.region_infer_pass { SymbolStorage, Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.semantic_analysis_pass { ExprCtx, Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.static_analysis_pass { ExprCtx, SymbolType }
    compiler.frontend.constant --> compiler.passes.static_analysis_pass.StaticAnalysisPass._check_client_imports { CodeContext }
    compiler.frontend.constant --> compiler.passes.sym_tab_build_pass { SymbolAccess }
    compiler.frontend.constant --> compiler.passes.sym_tab_build_pass.SymTabBuildPass.exit_binary_expr { Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.type_checker_pass { ImmutabilityKind, Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.type_checker_pass.TypeCheckPass._check_c_interop_import { is_borrow_kind }
    compiler.frontend.constant --> compiler.passes.type_checker_pass.TypeCheckPass._install_client_state_setters { client_state_setter_name }
    compiler.frontend.constant --> compiler.passes.type_checker_pass.TypeCheckPass.exit_ability { OwnershipKind }
    compiler.frontend.constant --> compiler.passes.type_checker_pass.TypeCheckPass.exit_impl_def { Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.variant_agreement_pass { SymbolAccess }
    compiler.frontend.constant --> compiler.passes.wasm_contract { OwnershipKind }
    compiler.frontend.constant --> compiler.placement.placement { CodeContext, SymbolAccess, Tokens as Tok }
    compiler.frontend.constant --> compiler.placement.placement._references_browser_seed_global { BROWSER_SEED_GLOBALS }
    compiler.frontend.constant --> compiler.placement.placement_solver { CodeContext, Tokens as Tok }
    compiler.frontend.constant --> compiler.symbol_utils { CodeContext, SymbolType, Tokens as Tok }
    compiler.frontend.constant --> compiler.symbol_utils.report_placement_warnings { CodeContext }
    compiler.frontend.constant --> compiler.tools.comment_attach_pass { Tokens as Tok }
    compiler.frontend.constant --> compiler.tools.doc_ir_gen_pass { Tokens as Tok, is_mut_kind }
    compiler.frontend.constant --> compiler.tools.jac_auto_lint_pass { TOKEN_MAP, Tokens as Tok }
    compiler.frontend.constant --> compiler.tools.normalize_pass { CodeContext }
    compiler.frontend.constant --> compiler.tools.reactive_use_walk { ExprCtx }
    compiler.frontend.constant --> compiler.tools.unparse_pass { OwnershipKind, is_mut_kind }
    compiler.frontend.constant --> compiler.types.builtin_extensions { SymbolAccess, SymbolType, Tokens }
    compiler.frontend.constant --> compiler.types.ct_eval { CodeContext, OwnershipKind, Tokens as Tok }
    compiler.frontend.constant --> compiler.types.fixed_width { TOKEN_MAP, Tokens as Tok }
    compiler.frontend.constant --> compiler.types.operations { Tokens as Tok }
    compiler.frontend.constant --> compiler.types.stubcat.reader { BindingKind, ImmutabilityKind, OwnershipKind, SymbolAccess, SymbolType, Tokens as Tok }
    compiler.frontend.constant --> compiler.types.stubcat.writer { BindingKind, ImmutabilityKind }
    compiler.frontend.constant --> compiler.types.ts_decl_parser { BindingKind }
    compiler.frontend.constant --> compiler.types.type_evaluator { BindingKind, CodeContext, ExprCtx, ImmutabilityKind, OwnershipKind, SymbolAccess, SymbolType, TOKEN_MAP, Tokens as Tok }
    compiler.frontend.constant --> compiler.types.type_evaluator.TypeEvaluator._collect_return_types { Tokens as _Tok }
    compiler.frontend.constant --> compiler.types.type_evaluator.TypeEvaluator._find_predicate_for { Tokens as Tok }
    compiler.frontend.constant --> compiler.types.type_evaluator.TypeEvaluator._merge_catalog_field_params { SymbolType }
    compiler.frontend.constant --> compiler.types.type_evaluator.TypeEvaluator._scope_has_fields { SymbolType }
    compiler.frontend.constant --> compiler.types.type_evaluator.TypeEvaluator.assign_type { SymbolType as _RtSymT }
    compiler.frontend.constant --> compiler.types.type_evaluator.TypeEvaluator.classify_condition { Tokens as Tok }
    compiler.frontend.constant --> compiler.types.type_utils { Tokens as Tok }
    compiler.frontend.constant --> compiler.types.type_utils._method_entry_of { SymbolType }
    compiler.frontend.constant --> compiler.types.types.ClassType.is_edge_type { SymbolType }
    compiler.frontend.constant --> compiler.types.types.ClassType.is_node_type { SymbolType }
    compiler.frontend.constant --> compiler.types.types.ClassType.is_walker_type { SymbolType }
    compiler.frontend.constant --> dist.publish.builder._module_is_client_source { CodeContext }
    compiler.frontend.constant --> lsp.server.engine { SymbolType, TOKEN_MAP }
    compiler.frontend.constant --> lsp.server.server { JacSemTokenModifier as SemTokMod, JacSemTokenType as SemTokType }
    compiler.frontend.constant --> server.hmr { CodeContext }
    compiler.frontend.constant --> testing.cl_test_runner.module_is_client { CodeContext }
    compiler.frontend.diagnostic_utils --> cli.commands.analysis.check { resolve_diagnostic_tokens }
    compiler.frontend.diagnostic_utils --> compiler.driver.pass_driver.diagnostic_policy_for { resolve_diagnostic_tokens }
    compiler.frontend.diagnostic_utils --> compiler.passes.context { resolve_diagnostic_tokens }
    compiler.frontend.diagnostics --> client.client_diagnostics._diag { DIAGNOSTICS }
    compiler.frontend.diagnostics --> compiler.backends.es.backends.registry { E5081 }
    compiler.frontend.diagnostics --> compiler.backends.es.esast_gen_pass { E2025, E5010, E5011, E5012, E5016, E5017, E5018, E5080, E5081, E5085, E5086, E5097, E5099, E5101, E5103, W5013, W5014, W5015 }
    compiler.frontend.diagnostics --> compiler.backends.es.esast_gen_pass.EsastGenPass._build_edge_ref { E5097 }
    compiler.frontend.diagnostics --> compiler.backends.es.esast_gen_pass.EsastGenPass._build_osp_filter_pred { E5097 }
    compiler.frontend.diagnostics --> compiler.backends.es.esast_gen_pass.EsastGenPass._build_server_forwarder { W6009 }
    compiler.frontend.diagnostics --> compiler.backends.es.esast_gen_pass.EsastGenPass._edge_tag_literal { E5097 }
    compiler.frontend.diagnostics --> compiler.backends.es.esast_gen_pass.EsastGenPass._ensure_backend { E5081 }
    compiler.frontend.diagnostics --> compiler.backends.es.esast_gen_pass.EsastGenPass._get_ast_or_default { E5097 }
    compiler.frontend.diagnostics --> compiler.backends.es.esast_gen_pass.EsastGenPass._warn_rpc_callable_params { W6005 }
    compiler.frontend.diagnostics --> compiler.backends.es.esast_gen_pass.EsastGenPass.prepare { E5096 }
    compiler.frontend.diagnostics --> compiler.backends.native.na_compile_pass { E5020, E5026 }
    compiler.frontend.diagnostics --> compiler.backends.native.na_ir_gen_pass { DiagnosticInfo, E5026, E5088, E5089, E5090, E5091, E5092, E5095, E9001, E9002 }
    compiler.frontend.diagnostics --> compiler.backends.native.primitives_native { E5092 }
    compiler.frontend.diagnostics --> compiler.backends.py.jcir_bc_gen_pass { E5040, E5043 }
    compiler.frontend.diagnostics --> compiler.backends.py.jcir_gen_pass { E5001, E5002, E5003, E5004, E5005, E5006, E5007, E5008, E5094, E5098, E5102, W5096 }
    compiler.frontend.diagnostics --> compiler.driver.ifacecache._alert_from_record { DIAGNOSTICS }
    compiler.frontend.diagnostics --> compiler.frontend.diagnostic_utils.resolve_diagnostic_tokens { DIAGNOSTICS, LINT_ALIASES }
    compiler.frontend.diagnostics --> compiler.frontend.parser.frontend { DIAGNOSTICS }
    compiler.frontend.diagnostics --> compiler.native_compiler.NativeCompiler.take_pass_results { DIAGNOSTICS }
    compiler.frontend.diagnostics --> compiler.passes.access_check_pass { E2034, E2035, E2037, E2038, E2039, W2034, W2035, W2037, W2038, W2039 }
    compiler.frontend.diagnostics --> compiler.passes.ast_validation_pass { E0010, E0020, E0023, E0024, E0031, E0040, E0041, E0042, E0043, E0044, E0050, E0051, E0052, E0055, E0058, E0059, E0063, E0065, E0066, E0067, E0071, E0075, E0076, E0082, E0083, E2019, E2020, E2021, E2022, E2024, E2084, W2019, W2020, W2021 }
    compiler.frontend.diagnostics --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._check_app_cycle { E5104 }
    compiler.frontend.diagnostics --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._check_provider_pub { E5106 }
    compiler.frontend.diagnostics --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._register_na_client_import { E5083, E5100 }
    compiler.frontend.diagnostics --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._reject_owned_type_import { E5108 }
    compiler.frontend.diagnostics --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass.enter_atom_trailer { E5112 }
    compiler.frontend.diagnostics --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass.enter_func_call { E5110 }
    compiler.frontend.diagnostics --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass.finish { E5093 }
    compiler.frontend.diagnostics --> compiler.passes.capability_check_pass { E5096, W6001, W6002, W6003, W6004 }
    compiler.frontend.diagnostics --> compiler.passes.context { DiagnosticInfo, E9001, LINT_ALIASES, Severity }
    compiler.frontend.diagnostics --> compiler.passes.decl_impl_match_pass { E2009, E2011, E2012, E2013, E2016, E2017, E2026, E2087, W2080 }
    compiler.frontend.diagnostics --> compiler.passes.decl_impl_match_pass.DeclImplMatchPass._connect_one_impl { E0064 }
    compiler.frontend.diagnostics --> compiler.passes.decl_impl_match_pass.DeclImplMatchPass._populate_inline_init_symbols { W2080 }
    compiler.frontend.diagnostics --> compiler.passes.decl_impl_match_pass.DeclImplMatchPass._populate_self_member_symbols { W2080 }
    compiler.frontend.diagnostics --> compiler.passes.graph_lowering_pass { E0084, E0085 }
    compiler.frontend.diagnostics --> compiler.passes.import_wiring_pass { E1141, E1142, E1143, E1144, E2088, E2089, E2090, E2091, E2092, E2093, E2094, W2083 }
    compiler.frontend.diagnostics --> compiler.passes.jsx_intrinsic_guard_pass { E1105 }
    compiler.frontend.diagnostics --> compiler.passes.layout_pass { E5030, W5031, W5032 }
    compiler.frontend.diagnostics --> compiler.passes.ownership_check_pass { E1301, E1302, E1303, E1304, E1305, E1306, E1307, E1308, E1309, E1311, E1313, E1314, E1315, E1316, E1317, E1318, E1320, E1321, E1322, E1323, E1401, E1402, E1403, E1404, E1405, E1406, W1310, W1312 }
    compiler.frontend.diagnostics --> compiler.passes.ownership_check_pass.OwnershipCheckPass._emit_place_intrinsic_diagnostics { E1319 }
    compiler.frontend.diagnostics --> compiler.passes.ownership_check_pass.OwnershipCheckPass._emit_raises_diagnostics { E1407 }
    compiler.frontend.diagnostics --> compiler.passes.pyast_load_pass { E5041, E5042 }
    compiler.frontend.diagnostics --> compiler.passes.semantic_analysis_pass { E2004, E2005, E2008, W2006, W2007, W2029 }
    compiler.frontend.diagnostics --> compiler.passes.static_analysis_pass { E1122, E1123, E1125, E2018, E2027, E2055, E2083, E2085, E2086, W1103, W2001, W2002, W2003, W2058, W2063, W2070, W2074, W2075 }
    compiler.frontend.diagnostics --> compiler.passes.static_analysis_pass.StaticAnalysisPass._check_client_imports { W1105, W1106 }
    compiler.frontend.diagnostics --> compiler.passes.sym_tab_build_pass { E0064, E0077 }
    compiler.frontend.diagnostics --> compiler.passes.type_checker_pass { Category, DiagnosticInfo, E0033, E0108, E0109, E1001, E1002, E1003, E1004, E1005, E1010, E1011, E1020, E1021, E1022, E1036, E1042, E1060, E1061, E1090, E1091, E1092, E1093, E1094, E1095, E1106, E1107, E1109, E1112, E1113, E1116, E1117, E1119, E1124, E1132, E1133, E1135, E1150, E1151, E1152, E2015, W1036, W1037, W1052, W2014, W6008 }
    compiler.frontend.diagnostics --> compiler.passes.variant_agreement_pass { E5105 }
    compiler.frontend.diagnostics --> compiler.placement.placement_solver { DiagnosticInfo }
    compiler.frontend.diagnostics --> compiler.placement.placement_solver._warn_state_forks { W6006 }
    compiler.frontend.diagnostics --> compiler.symbol_utils { E5082, E5084, W6006, W6007 }
    type compiler.frontend.diagnostics --> compiler.symbol_utils { DiagnosticInfo }
    compiler.frontend.diagnostics --> compiler.symbol_utils.report_serverless_kind_errors { E5087 }
    compiler.frontend.diagnostics --> compiler.tools.jac_auto_lint_pass { E3012, W3001, W3002, W3003, W3004, W3005, W3007, W3008, W3009, W3010, W3013, W3020, W3021, W3022, W3023, W3024, W3025, W3030, W3035, W3036, W3037, W3038, W3039, W3040, W3041, W3042, W3043, W3050, W3051, W3052, W3053 }
    compiler.frontend.diagnostics --> compiler.tools.jac_auto_lint_pass.JacAutoLintPass._check_filter_compare_tautology { W3040 }
    compiler.frontend.diagnostics --> compiler.tools.jac_formatter_pass { E5051, W5050 }
    compiler.frontend.diagnostics --> compiler.types.enum_utils { E1001 }
    compiler.frontend.diagnostics --> compiler.types.fixed_width { E1126, E1127, E1128, E1130 }
    compiler.frontend.diagnostics --> compiler.types.operations { E1010, E1033, E1035, E1055, E1096, E1097, E1098, E1114, E1115, E1118 }
    compiler.frontend.diagnostics --> compiler.types.type_evaluator { DiagnosticInfo, E0033, E0049, E0108, E0109, E1001, E1002, E1010, E1023, E1030, E1031, E1032, E1033, E1034, E1035, E1038, E1040, E1041, E1043, E1044, E1050, E1051, E1052, E1053, E1054, E1055, E1056, E1057, E1062, E1063, E1064, E1065, E1070, E1071, E1072, E1073, E1080, E1081, E1096, E1097, E1098, E1099, E1100, E1101, E1102, E1103, E1104, E1110, E1111, E1120, E1121, E1129, E1131, E1134, E1136, E1137, E1138, E1139, E5094, W1050, W1051, W1053, W1100, W1101, W1102, W2081, W2082 }
    compiler.frontend.helpers --> compiler.types.stubcat.writer { evaluate_version_condition }
    compiler.frontend.helpers --> compiler.types.type_utils.collect_member_syms { evaluate_version_condition }
    compiler.frontend.module_facts --> compiler.backends.es.esast_gen_pass { ModuleFacts }
    compiler.frontend.module_facts --> compiler.backends.es.esast_gen_pass.EsastGenPass.prepare { ModuleFacts, client_capability_violations }
    compiler.frontend.module_facts --> compiler.backends.native.na_ir_gen_pass { ModuleFacts }
    compiler.frontend.module_facts --> compiler.backends.py.jcir_gen_pass { ModuleFacts }
    compiler.frontend.module_facts --> compiler.passes.capability_check_pass { ModuleFacts, client_capability_violations }
    compiler.frontend.module_facts --> compiler.passes.import_wiring_pass { ModuleFacts }
    compiler.frontend.module_facts --> compiler.passes.osp_analysis { ModuleFacts }
    compiler.frontend.module_facts --> compiler.passes.type_checker_pass.TypeCheckPass.exit_ability { ModuleFacts }
    compiler.frontend.module_facts --> compiler.passes.type_checker_pass.TypeCheckPass.exit_return_stmt { ModuleFacts }
    compiler.frontend.module_facts --> compiler.tests.test_module_exports { ModuleFacts }
    compiler.frontend.module_facts --> compiler.types.type_evaluator.TypeEvaluator._init_prelude_from_sources { ModuleFacts }
    compiler.frontend.module_facts --> compiler.types.type_evaluator.TypeEvaluator.get_type_of_ability { ModuleFacts }
    compiler.frontend.parser --> cli.commands.fix._parse_module { parse as rd_parse }
    compiler.frontend.parser --> cli.commands.fix._parses_clean { parse as rd_parse }
    compiler.frontend.parser --> compiler.driver.compiler.JacCompiler._prepare_tool_program { parse as rd_parse }
    compiler.frontend.relations --> compiler.driver.program { ScopeChild }
    compiler.frontend.relations --> compiler.driver.progstate { ScopeChild }
    compiler.frontend.relations --> compiler.frontend.unitree { Absorbs, CalleeDecl, CfgFalse, CfgSucc, CfgTrue, Codespace, DecidedCodespace, Defines, EventTriggerOf, InScope, NarrowedTypeOf, PlacedIn, ScopeChild, ScopeOverload, ScopeParent, ScopePrimary, SymOf, TypeOf, Uses, codespace_node }
    compiler.frontend.relations --> compiler.passes.scope_walk { ScopeChild }
    compiler.frontend.relations --> compiler.types.types { BaseOf, BoundOf, ConstraintOf, DeclScopeOf, EnumClassOf, EnumMemberOf, GuardOf, MemberInfoOf, MroOf, OverloadOf, ParamDefaultOf, ParamOf, ParamTypeOf, PrivOf, ReturnsOf, SharedOf, TypeArgOf, TypeMemberOf, TypeParamOf, UnionMemberOf, ValueTypeOf }
    compiler.frontend.roles --> compiler.backends.es.esast_gen_pass { Kid }
    compiler.frontend.roles --> compiler.backends.native.na_ir_gen_pass { Kid }
    compiler.frontend.roles --> compiler.backends.py.jcir_gen_pass { Kid }
    compiler.frontend.roles --> compiler.driver.program { Kid }
    compiler.frontend.roles --> compiler.driver.progstate { Kid }
    compiler.frontend.roles --> compiler.driver.wiring { BodyRole, Kid }
    compiler.frontend.roles --> compiler.frontend.module_facts { Kid }
    compiler.frontend.roles --> compiler.frontend.parser.parser { Kid }
    compiler.frontend.roles --> compiler.frontend.unitree { AccessRole, AccessorsRole, AliasRole, ArchTagInfoRole, ArchTypeRole, ArgPatternsRole, AssignmentsRole, AssignsRole, AttributesRole, AugOpRole, AwaitingBodyRole, BaseClassesRole, BodyRole, BoundRole, CasesRole, CastTypeRole, CauseRole, ChainRole, ChildrenRole, ClibDeclsRole, CodeRole, CollectionRole, ComparesRole, ComprRole, ConditionRole, ConditionalRole, ConnAssignRole, ConnTypeRole, ConsumersRole, CountByRole, CtrlRole, DecoratorsRole, DefaultValRole, DescriptionRole, DocRole, DynamicTagRole, EdgeSpecRole, ElseBodyRole, ElseValueRole, EndRole, ErrorMsgRole, EventRole, ExTypeRole, ExceptsRole, ExprRole, ExprsRole, FTypeRole, FilterCondRole, FinallyBodyRole, FormatPartRole, FormatSpecRole, FromLocRole, FromTargetRole, GuardRole, HintRole, ImplOf, InsertLocRole, ItemsRole, IterRole, KeyRole, KeywordsRole, Kid, KvPairRole, KvPairsRole, KwPatternsRole, KwargsRole, KwonlyargsRole, LeftRole, MainRole, NameRefRole, NameRole, OpRole, OperandRole, OpsRole, OutExprRole, ParamsRole, PartsRole, PathRole, PatternPathRole, PatternRole, PatternsRole, PosonlyParamsRole, ProviderRole, ReturnTypeRole, RightRole, RightsRole, Role, ScopeRole, SignatureRole, SlicesRole, SourcesRole, SpecRole, SrcEndpointRole, StartRole, StepRole, StopRole, StringsRole, TargetRole, TargetsRole, TgtEndpointRole, TokRole, TypeCtxRole, TypeParamsRole, TypeTagRole, UnpackRole, ValueRole, ValueTypeRole, ValuesRole, VarargsRole, VarsRole }
    compiler.frontend.roles --> compiler.jc_unit { AccessorsRole, BodyRole, SpecRole }
    compiler.frontend.roles --> compiler.native_compiler.NativeCompiler._register { AccessorsRole, BodyRole, SpecRole }
    compiler.frontend.roles --> compiler.passes.annex_weave { BodyRole }
    compiler.frontend.roles --> compiler.passes.ast_validation_pass { Kid }
    compiler.frontend.roles --> compiler.passes.boundary_analysis_pass { Kid }
    compiler.frontend.roles --> compiler.passes.capability_check_pass { Kid }
    compiler.frontend.roles --> compiler.passes.cfg_build_pass { Kid }
    compiler.frontend.roles --> compiler.passes.comptime_resolve_pass { Kid }
    compiler.frontend.roles --> compiler.passes.endpoint_effect_pass { Kid }
    compiler.frontend.roles --> compiler.passes.osp_analysis { Kid }
    compiler.frontend.roles --> compiler.passes.ownership_check_pass { Kid }
    compiler.frontend.roles --> compiler.passes.pyast_load_pass { Kid, NameRefRole, ReturnTypeRole, UnpackRole, ValueRole }
    compiler.frontend.roles --> compiler.passes.region_infer_pass { BodyRole, Kid }
    compiler.frontend.roles --> compiler.passes.type_checker_pass { Kid }
    compiler.frontend.roles --> compiler.tools.comment_attach_pass { Kid }
    compiler.frontend.roles --> compiler.tools.doc_ir_gen_pass { Kid }
    compiler.frontend.roles --> compiler.tools.grammar_extract_pass { Kid }
    compiler.frontend.roles --> compiler.tools.jac_auto_lint_pass { AssignmentsRole, BodyRole, ConditionRole, DecoratorsRole, DocRole, ElseValueRole, ExprRole, ItemsRole, Kid, NameRefRole, ReturnTypeRole, SignatureRole, SpecRole, TargetRole, ValueRole, ValuesRole, VarsRole }
    compiler.frontend.roles --> compiler.tools.normalize_pass { BodyRole, ItemsRole, Kid }
    compiler.frontend.roles --> compiler.tools.reactive_use_walk { Kid, ValueRole }
    compiler.frontend.roles --> compiler.tools.treeprinter { Kid }
    compiler.frontend.roles --> compiler.tools.unparse_pass { Kid, Role }
    compiler.frontend.roles --> compiler.types.operations { Kid }
    compiler.frontend.roles --> compiler.types.stubcat.writer { Kid }
    compiler.frontend.roles --> compiler.types.type_evaluator { Kid }
    compiler.frontend.srcloc --> compiler.driver.ifacecache._span_from_record { Span }
    compiler.frontend.srcloc --> compiler.frontend.codeinfo { CodeLocInfo }
    compiler.frontend.srcloc --> compiler.frontend.parser.frontend { Span }
    compiler.frontend.srcloc --> compiler.frontend.unitree { CodeLocInfo }
    compiler.frontend.srcloc --> compiler.passes.context { CodeLocInfo, Span }
    compiler.frontend.srcloc --> lsp.server.utils { Span }
    type compiler.frontend.srcloc --> project.source { Span }
    compiler.frontend.unitree --> cli.commands.analysis._check_file_job { Source as _Src }
    compiler.frontend.unitree --> cli.commands.architecture { GraphImport, Import, ImportRule, ImportWire, ModuleItem, ModulePath }
    compiler.frontend.unitree as uni --> cli.commands.fix._access_plan;
    compiler.frontend.unitree as uni --> cli.commands.fix._imported_names;
    compiler.frontend.unitree as uni --> cli.commands.fix._module_has_jsx;
    compiler.frontend.unitree as uni --> cli.commands.fix._plain_top_decls;
    compiler.frontend.unitree as uni --> cli.commands.fix._priv_top_decls;
    compiler.frontend.unitree as uni --> cli.commands.transform.py2jac;
    type compiler.frontend.unitree --> client.client_bundle { Module }
    compiler.frontend.unitree as uni --> compiler.backends.es.esast_gen_pass;
    compiler.frontend.unitree as uni --> compiler.backends.es.jsx_processor;
    compiler.frontend.unitree as uni --> compiler.backends.es.view_ir;
    type compiler.frontend.unitree --> compiler.backends.native.entry_points { Module }
    compiler.frontend.unitree as uni --> compiler.backends.native.foreign;
    compiler.frontend.unitree as uni --> compiler.backends.native.na_compile_pass;
    compiler.frontend.unitree as uni --> compiler.backends.native.na_ir_gen_pass;
    compiler.frontend.unitree --> compiler.backends.native.primitives_native { Expr, UniNode }
    type compiler.frontend.unitree --> compiler.backends.native.wasm_build { Module as UniModule }
    compiler.frontend.unitree --> compiler.backends.py.jcir_bc_gen_pass { Module }
    compiler.frontend.unitree --> compiler.backends.py.jcir_gen_pass { Ability, ArchHas, Archetype, AssertStmt, AssignCompr, Assignment, AstSymbolNode, AtomTrailer, AtomUnit, AwaitExpr, BinaryExpr, Bool, BoolExpr, BuiltinType, CastExpr, CfgExpr, CodeBlockStmt, CommentToken, CompareExpr, ConcurrentExpr, ConnectOp, ContextAwareNode, CtrlStmt, DeleteStmt, DictCompr, DictVal, DisconnectOp, DisengageStmt, EdgeOpRef, EdgeRefTrailer, Ellipsis, ElseIf, ElseStmt, Enum, EnumBlockStmt, EventSignature, Except, Expr, ExprAsItem, ExprCtx, ExprStmt, FString, FilterCompr, FinallyStmt, Float, ForeverStmt, FormattedValue, FuncCall, FuncSignature, GenCompr, GlobalVars, HasVar, IfElseExpr, IfStmt, ImplDef, Import, InForStmt, IndexSlice, InnerCompr, Int, IterForStmt, JsxComment, JsxElement, JsxElementName, JsxExpression, JsxNormalAttribute, JsxSlot, JsxSpreadAttribute, JsxText, KVPair, KWPair, LambdaExpr, ListCompr, ListVal, MatchArch, MatchAs, MatchCase, MatchKVPair, MatchMapping, MatchOr, MatchPattern, MatchSequence, MatchSingleton, MatchStar, MatchStmt, MatchValue, MatchWild, Module, ModuleCode, ModuleItem, ModulePath, MultiString, Name, NameAtom, Null, OpenStmt, ParamVar, PyInlineCode, RaiseStmt, ReportStmt, ReturnStmt, SemDef, Semi, SetCompr, SetVal, SpecialVarRef, String, SubTag, SwitchStmt, Test, Token, TryStmt, TupleVal, TypeAlias, TypeParam, TypedCtxBlock, UnaryExpr, UniNode, UniScopeNode, VisitStmt, WhileStmt, WithStmt, YieldExpr, is_identifier_slot, literal_string_value }
    compiler.frontend.unitree --> compiler.c_interop { Archetype, Assignment, AtomTrailer, AtomUnit, Expr, Import, UnaryExpr, UniNode }
    compiler.frontend.unitree --> compiler.c_interop._annotation_name { Name, Null }
    compiler.frontend.unitree --> compiler.c_interop.c_call_borrows_args { FuncCall }
    compiler.frontend.unitree as uni --> compiler.driver.boundary_classify;
    compiler.frontend.unitree as uni --> compiler.driver.compiler;
    compiler.frontend.unitree --> compiler.driver.context_passes { Module }
    compiler.frontend.unitree as uni --> compiler.driver.ifacecache.IfaceRegistry._client_edges;
    type compiler.frontend.unitree --> compiler.driver.nativecache { Module }
    type compiler.frontend.unitree --> compiler.driver.pipeline { Module }
    compiler.frontend.unitree as uni --> compiler.driver.pipeline_runner;
    compiler.frontend.unitree as uni --> compiler.driver.program;
    compiler.frontend.unitree as uni --> compiler.driver.progstate;
    compiler.frontend.unitree as uni --> compiler.driver.selfhost;
    type compiler.frontend.unitree --> compiler.driver.source_products { Module }
    compiler.frontend.unitree --> compiler.driver.wiring { Ability, Archetype, EmptyToken, Enum, ImplDef, GraphImport, Import, ImportRule, ImportWire, Module, ModuleItem, ModulePath, ModulePattern, Token, UniNode }
    compiler.frontend.unitree --> compiler.expr_keys { Assignment, AtomTrailer, AtomUnit, BinaryExpr, BoolExpr, CfgExpr, CompareExpr, Expr, FuncCall, InForStmt, IndexSlice, Int, KWPair, ListVal, MultiString, Name, String, Token, TupleVal, UnaryExpr, UniNode }
    compiler.frontend.unitree --> compiler.expr_keys.type_tag_borrows { SubTag, UnaryExpr }
    compiler.frontend.unitree --> compiler.field_semantics { AstSymbolNode, Bool, Expr, FuncCall, HasVar, KWPair, Module, ModuleItem, Name }
    type compiler.frontend.unitree --> compiler.frontend.codeinfo { CommentToken }
    compiler.frontend.unitree --> compiler.frontend.const_fold { AtomUnit, BinaryExpr, Bool, Float, Int, MultiString, String, UnaryExpr, UniNode }
    type compiler.frontend.unitree --> compiler.frontend.helpers { Expr }
    compiler.frontend.unitree as uni --> compiler.frontend.helpers._extract_version_tuple;
    compiler.frontend.unitree as uni --> compiler.frontend.helpers._is_type_checking_ref;
    compiler.frontend.unitree as uni --> compiler.frontend.helpers._is_version_info_access;
    compiler.frontend.unitree as uni --> compiler.frontend.helpers.evaluate_version_condition;
    compiler.frontend.unitree --> compiler.frontend.module_facts { Ability, Archetype, Assignment, AtomTrailer, ConcurrentExpr, ContextAwareNode, ElementStmt, Enum, FuncCall, GlobalVars, ImplDef, Import, LambdaExpr, ListVal, Module, ModuleCode, ModuleItem, Name, TupleVal, UniNode, YieldExpr, literal_string_value }
    compiler.frontend.unitree --> compiler.frontend.parser.frontend { CommentToken, Expr, Module, Source }
    compiler.frontend.unitree --> compiler.frontend.parser.parser { Ability, ArchHas, Archetype, AssertStmt, AssignCompr, Assignment, AstDocNode, AtomTrailer, AtomUnit, AwaitExpr, AwaitingClause, BinaryExpr, Bool, BoolExpr, BuiltinType, CastExpr, CfgExpr, CodeBlockStmt, CompareExpr, ConcurrentExpr, ConnectOp, ContextAwareNode, CtrlStmt, DeleteStmt, DictCompr, DictVal, DisconnectOp, DisengageStmt, EdgeOpRef, EdgeRefTrailer, ElementStmt, Ellipsis as EllipsisLit, ElseIf, ElseStmt, EmptyToken, Enum, EventSignature, Except, Expr, ExprAsItem, ExprStmt, FString, FilterCompr, FinallyStmt, Float, ForeverStmt, FormattedValue, FuncCall, FuncSignature, GenCompr, GlobalVars, GraphExpr, HasVar, IfElseExpr, IfStmt, ImplDef, GraphImport, Import, ImportRule, ImportWire, InForStmt, IndexSlice, InnerCompr, Int, IterForStmt, JsxAttribute, JsxChild, JsxComment, JsxElement, JsxElementName, JsxExpression, JsxNormalAttribute, JsxSlot, JsxSpreadAttribute, JsxText, KVPair, KWPair, LambdaExpr, ListCompr, ListVal, MatchArch, MatchAs, MatchCase, MatchKVPair, MatchMapping, MatchOr, MatchPattern, MatchSequence, MatchSingleton, MatchStar, MatchStmt, MatchValue, MatchWild, Module, ModuleCode, ModuleItem, ModulePath, ModulePattern, MultiString, Name, NameAtom, Null, OpenStmt, ParamVar, PyInlineCode, RaiseStmt, ReportStmt, ReturnStmt, SemDef, Semi, SetCompr, SetVal, Slice, Source, SpecialVarRef, String, SubTag, SwitchCase, SwitchStmt, Test, Token, TryStmt, TupleVal, TypeAlias, TypeParam, TypedCtxBlock, UnaryExpr, UniNode, VisitStmt, WhileStmt, WireItem, WithStmt, YieldExpr }
    type compiler.frontend.unitree --> compiler.frontend.relations { Ability, AstTypedVarNode, ConditionalNode, ContextAwareNode, Expr, FuncCall, Import, Module, NameAtom, Symbol, UniCFGNode, UniScopeNode }
    type compiler.frontend.unitree --> compiler.frontend.roles { Ability, ArchHas, Archetype, AssertStmt, AssignCompr, Assignment, AstAccessNode, AstDocNode, AstElseBodyNode, AstTypedVarNode, AtomTrailer, AwaitingClause, CastExpr, CfgExpr, CompareExpr, ConcurrentExpr, ConnectOp, CtrlStmt, DictCompr, DictVal, DisconnectOp, EdgeOpRef, EdgeRefTrailer, ElseIf, ElseStmt, Enum, EventSignature, Except, Expr, ExprAsItem, FString, FilterCompr, FinallyStmt, FormattedValue, FuncSignature, GlobalVars, HasVar, IfElseExpr, ImplDef, GraphImport, Import, ImportRule, ImportWire, IndexSlice, InnerCompr, IterForStmt, JsxAttribute, JsxChild, JsxElement, JsxElementName, KVPair, KWPair, ListCompr, MatchArch, MatchCase, MatchKVPair, MatchOr, MatchPattern, Module, ModuleItem, ModulePath, ModulePattern, MultiString, Name, NameAtom, ParamVar, ProgramModule, PyInlineCode, RaiseStmt, Slice, String, SubTag, SwitchCase, Test, Token, TryStmt, TypeParam, TypedCtxBlock, UnaryExpr, UniNode, VisitStmt, WireItem }
    type compiler.frontend.unitree --> compiler.frontend.srcloc { Source, Token }
    compiler.frontend.unitree --> compiler.jc_unit { Import, Module }
    compiler.frontend.unitree --> compiler.passes.access_check_pass { Archetype, AstSymbolNode, AtomTrailer, Import, Module, ModuleItem, ModulePath, Name, Symbol, UniNode }
    compiler.frontend.unitree --> compiler.passes.annex_weave { Module }
    compiler.frontend.unitree --> compiler.passes.ast_validation_pass { Ability, ArchHas, Archetype, Assignment, AtomTrailer, AtomUnit, BinaryExpr, ContextAwareNode, CtrlStmt, DeleteStmt, ElseStmt, Enum, ExprAsItem, ExprStmt, FString, ForeverStmt, FuncCall, FuncSignature, GlobalVars, HasVar, IfStmt, ImplDef, Import, InForStmt, InnerCompr, IterForStmt, JsxElement, JsxNormalAttribute, JsxSlot, KWPair, LambdaExpr, ListVal, Literal, MatchStmt, Module, ModuleCode, MultiString, Name, ParamVar, ReturnStmt, SpecialVarRef, SwitchStmt, Token, TreeWalker, TryStmt, TupleVal, UnaryExpr, UniNode, WhileStmt, WithStmt, YieldExpr }
    compiler.frontend.unitree --> compiler.passes.boundary_analysis_pass { Ability, ArchHas, Archetype, Assignment, AstSymbolNode, AtomTrailer, BinaryExpr, Bool, BuiltinType, DictVal, Enum, Float, FuncCall, FuncSignature, HasVar, Import, IndexSlice, Int, KVPair, LambdaExpr, ListVal, Module, ModuleItem, ModulePath, MultiString, Name, NameAtom, Null, ParamVar, Slice, String, Token, TreeWalker, TupleVal, UnaryExpr, UniNode, ability_of_symbol, resolved_decl_of }
    compiler.frontend.unitree --> compiler.passes.capability_check_pass { Ability, ArchSpec, Archetype, Assignment, AtomTrailer, CtrlStmt, EdgeOpRef, EdgeRefTrailer, ElementStmt, Enum, EventSignature, Expr, FString, FilterCompr, FormattedValue, FuncCall, FuncSignature, ImplDef, GraphImport, Import, KWPair, LambdaExpr, ListVal, Module, ModuleItem, ModulePath, MultiString, Name, ParamVar, PyInlineCode, String, Token, TupleVal, UnaryExpr, UniNode, YieldExpr, in_type_position }
    compiler.frontend.unitree --> compiler.passes.cfg_build_pass { Ability, Archetype, AssertStmt, AstElseBodyNode, AtomUnit, AwaitingClause, BoolExpr, CfgExpr, CodeBlockStmt, CtrlStmt, DictCompr, DisengageStmt, ElseIf, ElseStmt, Except, Expr, FinallyStmt, ForeverStmt, GenCompr, GlobalVars, IfElseExpr, IfStmt, ImplDef, InForStmt, InnerCompr, IterForStmt, JsxSlot, LambdaExpr, ListCompr, MatchCase, MatchStmt, Module, ModuleCode, Name, OpenStmt, RaiseStmt, ReturnStmt, SemDef, Semi, SetCompr, SwitchCase, SwitchStmt, Test, Token, TreeWalker, TryStmt, TypeAlias, TypedCtxBlock, UniCFGNode, UniNode, WhileStmt, WithStmt }
    compiler.frontend.unitree --> compiler.passes.comptime_resolve_pass { Ability, AssertStmt, Assignment, GlobalVars, IfStmt, Import, InForStmt, ParamVar, TypeParam, UniNode }
    compiler.frontend.unitree --> compiler.passes.context { Source, UniNode }
    compiler.frontend.unitree --> compiler.passes.dataflow { UniCFGNode }
    compiler.frontend.unitree --> compiler.passes.decl_impl_match_pass { Ability, Archetype, Assignment, AstImplNeedingNode, AstSymbolNode, AtomTrailer, FuncSignature, HasVar, ImplDef, Import, Module, Name, NameAtom, ParamVar, SpecialVarRef, Symbol, UniNode, UniScopeNode, bind_assignment_targets, find_python_scope_node_of, is_identifier_slot }
    compiler.frontend.unitree --> compiler.passes.endpoint_effect_pass { Ability, Archetype, Assignment, AstSymbolNode, AtomTrailer, BinaryExpr, BoolExpr, ConnectOp, DeleteStmt, DisconnectOp, EventSignature, FuncCall, ImplDef, KWPair, Module, Name, SpecialVarRef, Symbol, Token, TreeWalker, UniNode, ability_of_symbol }
    compiler.frontend.unitree --> compiler.passes.execution { UniNode }
    compiler.frontend.unitree as uni --> compiler.passes.freeze_structure_pass;
    compiler.frontend.unitree as uni --> compiler.passes.graph_lowering_pass;
    compiler.frontend.unitree --> compiler.passes.graph_lowering_pass { TreeWalker }
    compiler.frontend.unitree --> compiler.passes.import_wiring_pass { Ability, EmptyToken, ImplDef, GraphImport, Import, ImportRule, ImportWire, Module, ModuleItem, ModulePath, ModulePattern, String, UniNode }
    compiler.frontend.unitree --> compiler.passes.jsx_intrinsic_guard_pass { JsxElement, Module, Name, Token, TreeWalker, UniNode }
    compiler.frontend.unitree --> compiler.passes.layout_pass { Ability, ArchHas, Archetype, Assignment, AstSymbolNode, AstTypedVarNode, AtomTrailer, BinaryExpr, BuiltinType, Enum, Expr, FuncCall, FuncSignature, HasVar, Import, IndexSlice, Module, ModuleItem, Name, Null, TupleVal, TypeParam, UnaryExpr, UniNode }
    compiler.frontend.unitree --> compiler.passes.mtir_gen_pass { Ability, Archetype, Assignment, AstSymbolNode, AtomTrailer, BinaryExpr, Bool, BuiltinType, EdgeOpRef, EdgeRefTrailer, Enum, EventSignature, Expr, FilterCompr, Float, FuncCall, FuncSignature, Int, KWPair, ListVal, Module, MultiString, Name, NameAtom, String, Symbol, Token, TupleVal, UniNode, UniScopeNode, VisitStmt }
    compiler.frontend.unitree as uni --> compiler.passes.osp_analysis;
    compiler.frontend.unitree --> compiler.passes.ownership_check_pass { Ability, Archetype, Assignment, AstElseBodyNode, AtomTrailer, BinaryExpr, CfgExpr, ConcurrentExpr, ConnectOp, CtrlStmt, DeleteStmt, DictVal, DisengageStmt, Enum as UniEnum, Except, Expr, FString, FinallyStmt, FuncCall, FuncSignature, GlobalVars, HasVar, IfElseExpr, ImplDef, Import, InForStmt, IndexSlice, Int, IterForStmt, KWPair, LambdaExpr, ListVal, Module, ModuleCode, MultiString, Name, Null, OpenStmt, ParamVar, RaiseStmt, ReturnStmt, SetVal, Slice, String, SubTag, Token, TryStmt, TupleVal, UnaryExpr, UniCFGNode, UniNode, UniScopeNode, WhileStmt, YieldExpr }
    compiler.frontend.unitree --> compiler.passes.ownership_hints { Ability, Assignment, FuncSignature, Module, Name }
    compiler.frontend.unitree --> compiler.passes.pyast_load_pass { Ability, ArchBlockStmt, Archetype, AssertStmt, Assignment, AtomExpr, AtomTrailer, AtomUnit, AwaitExpr, BinaryExpr, Bool, BoolExpr, CfgExpr, CodeBlockStmt, CompareExpr, CtrlStmt, DeleteStmt, DictCompr, DictVal, ElementStmt, Ellipsis as UniEllipsis, ElseIf, ElseStmt, EmptyToken, Enum, Except, Expr, ExprAsItem, ExprStmt, FString, FinallyStmt, Float, FormattedValue, FuncCall, FuncSignature, GenCompr, IfElseExpr, IfStmt, Import, InForStmt, IndexSlice, InnerCompr, Int, KVPair, KWPair, LambdaExpr, ListCompr, ListVal, Literal, MatchArch, MatchAs, MatchCase, MatchKVPair, MatchMapping, MatchOr, MatchPattern, MatchSequence, MatchSingleton, MatchStar, MatchStmt, MatchValue, MatchWild, Module, ModuleCode, ModuleItem, ModulePath, MultiString, Name, NameAtom, Null, ParamKind, ParamVar, PythonModuleAst, RaiseStmt, ReturnStmt, Semi, SetCompr, SetVal, Slice, Source, SpecialVarRef, String, SubTag, Token, TryStmt, TupleVal, UnaryExpr, UniNode, WhileStmt, WithStmt, YieldExpr }
    compiler.frontend.unitree --> compiler.passes.rc_facts_pass { Ability, Assignment, AtomTrailer, BinaryExpr, BoolExpr, CompareExpr, ConnectOp, DictCompr, DictVal, Expr, FString, FuncCall, FuncSignature, IfElseExpr, IfStmt, ImplDef, InForStmt, IterForStmt, KWPair, LambdaExpr, ListCompr, ListVal, Module, ModuleCode, MultiString, Name, NameAtom, ParamVar, ReturnStmt, SetVal, String, Symbol, Test, Token, UnaryExpr, UniCFGNode, UniNode, WhileStmt, same_lexical_scope }
    compiler.frontend.unitree --> compiler.passes.region_infer_pass { Ability, Archetype, Assignment, AtomTrailer, BinaryExpr, CodeBlockStmt, ConnectOp, CtrlStmt, ExprStmt, FuncCall, FuncSignature, ImplDef, KWPair, Module, ModuleCode, Name, NameAtom, OpenStmt, RaiseStmt, ReturnStmt, Symbol, Test, Token, UniNode, YieldExpr }
    compiler.frontend.unitree --> compiler.passes.scope_walk { UniScopeNode }
    compiler.frontend.unitree --> compiler.passes.sem_def_match_pass { Module, SemDef, Symbol, UniScopeNode }
    compiler.frontend.unitree --> compiler.passes.semantic_analysis_pass { Ability, ArchHas, Archetype, Assignment, AstSymbolNode, AtomExpr, AtomTrailer, DisengageStmt, EdgeOpRef, EventSignature, ExprAsItem, FuncSignature, HasVar, ImplDef, InForStmt, InnerCompr, Module, Name, ParamVar, SpecialVarRef, TreeWalker, TypedCtxBlock, UniNode, VisitStmt }
    compiler.frontend.unitree --> compiler.passes.static_analysis_pass { Ability, Archetype, Assignment, AtomTrailer, AwaitExpr, BinaryExpr, Bool, CompareExpr, ConnectOp, CtrlStmt, DisconnectOp, DisengageStmt, EdgeOpRef, ElseIf, ElseStmt, EventSignature, FString, FilterCompr, FinallyStmt, Float, ForeverStmt, FormattedValue, IfStmt, ImplDef, GraphImport, Import, InForStmt, Int, IterForStmt, KWPair, LambdaExpr, MatchPattern, Module, ModuleItem, ModulePath, Name, Null, RaiseStmt, ReturnStmt, Semi, Test, Token, UniNode, UniScopeNode, WhileStmt, in_type_position }
    compiler.frontend.unitree --> compiler.passes.sym_tab_build_pass { Ability, ArchHas, Archetype, Assignment, AstSymbolNode, AtomTrailer, BinaryExpr, DictCompr, ElseIf, ElseStmt, Enum, Except, ExprAsItem, FinallyStmt, ForeverStmt, GenCompr, GlobalVars, HasVar, IfStmt, ImplDef, Import, InForStmt, InnerCompr, IterForStmt, LambdaExpr, ListCompr, MatchCase, Module, ModuleItem, ModulePath, Name, OpenStmt, ParamVar, SemDef, SetCompr, SwitchCase, Symbol, Test, Token, TreeWalker, TryStmt, TypeAlias, TypeParam, TypedCtxBlock, UniNode, UniScopeNode, WhileStmt, WithStmt, bind_assignment_targets, def_insert_unpacking, find_python_scope_node_of, rebind_or_def_insert, record_cross_scope_rebind }
    compiler.frontend.unitree --> compiler.passes.type_checker_pass { Ability, ArchHas, Archetype, AssertStmt, Assignment, AstSymbolNode, AtomTrailer, BinaryExpr, BuiltinType, CodeBlockStmt, CompareExpr, DeleteStmt, EdgeRefTrailer, ElseIf, Enum, EventSignature, Except, Expr, ExprAsItem, FString, FilterCompr, FormattedValue, FuncCall, FuncSignature, GenCompr, HasVar, IfStmt, ImplDef, Import, ImportRule, InForStmt, IndexSlice, JsxElement, JsxElementName, KWPair, LambdaExpr, ListVal, Literal, MatchAs, Module, ModuleCode, ModuleItem, ModulePath, MultiString, Name, Null, ParamVar, RaiseStmt, ReportStmt, ReturnStmt, Slice, SpecialVarRef, SubTag, Symbol, Token, TreeWalker, TupleVal, TypeAlias, UnaryExpr, UniNode, VisitStmt, WhileStmt, WireItem, WithStmt, YieldExpr, find_python_scope_node_of, in_type_position, type_only_import_of }
    compiler.frontend.unitree --> compiler.passes.variant_agreement_pass { Ability, Archetype, Enum, FuncSignature, GlobalVars, HasVar, Module, Name, UniNode }
    compiler.frontend.unitree --> compiler.passes.wasm_contract { Ability, FuncSignature, UnaryExpr }
    compiler.frontend.unitree --> compiler.passes.wasm_contract.check_host_call { Module, Name, ability_of_symbol }
    compiler.frontend.unitree --> compiler.passes.wasm_contract.host_contracts { Import }
    compiler.frontend.unitree as uni --> compiler.placement.placement;
    compiler.frontend.unitree as uni --> compiler.placement.placement_facts;
    compiler.frontend.unitree as uni --> compiler.placement.placement_solver;
    compiler.frontend.unitree as uni --> compiler.placement.placement_work;
    compiler.frontend.unitree --> compiler.symbol_utils { Ability, Archetype, Assignment, AstSymbolNode, AtomTrailer, BinaryExpr, ContextAwareNode, ElementStmt, Enum as UniEnum, Expr, FuncCall, GlobalVars, HasVar, Import, KWPair, Module, ModuleItem, ModulePath, Name, NameAtom, ParamVar, Symbol, Token, UniNode, UniScopeNode, ability_of_symbol, in_type_position }
    compiler.frontend.unitree --> compiler.tests.test_client_codegen_facts { Module }
    compiler.frontend.unitree --> compiler.tests.test_jac_mobui_typing { Import, ModuleItem, Name }
    compiler.frontend.unitree --> compiler.tests.test_module_exports { Module, PythonModuleAst, Source }
    compiler.frontend.unitree --> compiler.tests.test_pipeline_products { Module }
    compiler.frontend.unitree --> compiler.tests.test_test_block_analysis { FuncCall, Module, Name, Test }
    compiler.frontend.unitree as uni --> compiler.tools.code_intel;
    compiler.frontend.unitree as uni --> compiler.tools.comment_attach_pass;
    type compiler.frontend.unitree as uni --> compiler.tools.doc_ir;
    compiler.frontend.unitree as uni --> compiler.tools.doc_ir_gen_pass;
    compiler.frontend.unitree --> compiler.tools.doc_ir_gen_pass { TreeWalker }
    compiler.frontend.unitree as uni --> compiler.tools.grammar_extract_pass;
    compiler.frontend.unitree --> compiler.tools.grammar_extract_pass { TreeWalker }
    compiler.frontend.unitree as uni --> compiler.tools.jac_auto_lint_pass;
    compiler.frontend.unitree --> compiler.tools.jac_auto_lint_pass { TreeWalker }
    compiler.frontend.unitree as uni --> compiler.tools.jac_formatter_pass;
    compiler.frontend.unitree as uni --> compiler.tools.lang_tools;
    compiler.frontend.unitree --> compiler.tools.lang_tools { UniScopeNode }
    compiler.frontend.unitree as uni --> compiler.tools.normalize_pass;
    compiler.frontend.unitree --> compiler.tools.normalize_pass { EmptyToken, Tok, Token, TreeWalker }
    compiler.frontend.unitree as uni --> compiler.tools.reactive_use_walk;
    compiler.frontend.unitree as uni --> compiler.tools.treeprinter;
    type compiler.frontend.unitree --> compiler.tools.treeprinter { UniNode, UniScopeNode }
    compiler.frontend.unitree --> compiler.tools.treeprinter.print_ast_tree { AstSymbolNode, Token }
    compiler.frontend.unitree as uni --> compiler.tools.unparse_pass;
    compiler.frontend.unitree --> compiler.tools.unparse_pass { TreeWalker }
    compiler.frontend.unitree --> compiler.types.builtin_extensions { Name, Source }
    compiler.frontend.unitree --> compiler.types.ct_eval { Ability, Archetype, AssertStmt, Assignment, AtomTrailer, AtomUnit, BinaryExpr, Bool, BoolExpr, BuiltinType, CastExpr, CfgExpr, CompareExpr, CtrlStmt, DictCompr, DictVal, ElseIf, ElseStmt, Enum, Expr, ExprStmt, FString, Float, FormattedValue, FuncCall, FuncSignature, GlobalVars, HasVar, IfElseExpr, IfStmt, ImplDef, Import, InForStmt, IndexSlice, InnerCompr, Int, KVPair, KWPair, ListCompr, ListVal, Module, ModuleItem, ModulePath, MultiString, Name, Null, ParamVar, RaiseStmt, ReturnStmt, Semi, SetCompr, SetVal, Slice, SpecialVarRef, String, Symbol, Token, TryStmt, TupleVal, TypeParam, UnaryExpr, UniNode, WhileStmt }
    type compiler.frontend.unitree --> compiler.types.ct_value { Ability }
    compiler.frontend.unitree --> compiler.types.enum_utils { Ability, Archetype, Assignment, Enum, Int, Name, NameAtom, String, UniNode }
    compiler.frontend.unitree --> compiler.types.fixed_width { AtomUnit, Expr, Float, FuncCall, Int, Name, Token, UnaryExpr, UniNode }
    compiler.frontend.unitree --> compiler.types.operations { AtomTrailer, BinaryExpr, ConnectOp, DisconnectOp, Expr, FuncCall, KWPair, Name, Token, TupleVal, UniNode }
    compiler.frontend.unitree --> compiler.types.ownership { Archetype, HasVar }
    compiler.frontend.unitree --> compiler.types.stubcat.modiface { Module }
    compiler.frontend.unitree --> compiler.types.stubcat.reader { Ability, HasVar, Module, Name, Source, Symbol, SymbolProvider, Token, UniNode, UniScopeNode }
    compiler.frontend.unitree --> compiler.types.stubcat.writer { Ability, Archetype, Assignment, AtomTrailer, DictCompr, ElseIf, ElseStmt, Enum, FuncSignature, HasVar, IfStmt, Import, InnerCompr, KWPair, ListCompr, Module, ModulePath, Name, ParamVar, Symbol, UniScopeNode }
    compiler.frontend.unitree --> compiler.types.type_evaluator { Ability, Archetype, AssertStmt, AssignCompr, Assignment, AtomTrailer, AtomUnit, AwaitExpr, BinaryExpr, Bool, BoolExpr, BuiltinType, CastExpr, CfgExpr, CodeBlockStmt, CompareExpr, ConcurrentExpr, CtrlStmt, DictCompr, DictVal, EdgeOpRef, EdgeRefTrailer, Ellipsis, ElseIf, ElseStmt, Enum, EventSignature, Except, Expr, ExprAsItem, ExprStmt, FString, FilterCompr, Float, ForeverStmt, FormattedValue, FuncCall, FuncSignature, GenCompr, HasVar, IfElseExpr, IfStmt, ImplDef, Import, InForStmt, IndexSlice, InnerCompr, Int, IterForStmt, JsxComment, JsxElement, JsxElementName, JsxExpression, JsxNormalAttribute, JsxSpreadAttribute, JsxText, KVPair, KWPair, LambdaExpr, ListCompr, ListVal, MatchArch, MatchAs, MatchCase, MatchOr, MatchPattern, MatchStmt, MatchWild, Module, ModuleItem, ModulePath, MultiString, Name, NameAtom, Null, OpenStmt, ParamVar, RaiseStmt, ReturnStmt, Semi, SetCompr, SetVal, Source, SpecialVarRef, String, SubTag, SwitchCase, SwitchStmt, Symbol, Token, TryStmt, TupleVal, TypeAlias, TypeParam, UnaryExpr, UniCFGNode, UniNode, UniScopeNode, WhileStmt, WithStmt, YieldExpr, is_client_destined, kind_has_runtime_binding, literal_string_value, resolved_decl_of }
    compiler.frontend.unitree --> compiler.types.type_evaluator.TypeEvaluator._container_value_type { in_type_position }
    compiler.frontend.unitree --> compiler.types.type_evaluator.TypeEvaluator._get_type_of_expression_core { in_type_position }
    compiler.frontend.unitree --> compiler.types.type_evaluator.TypeEvaluator._heal_class_bases { Archetype }
    compiler.frontend.unitree --> compiler.types.type_evaluator.TypeEvaluator._published_class_type { Archetype }
    compiler.frontend.unitree --> compiler.types.type_evaluator.TypeEvaluator._resolve_string_type_expr { SubTag }
    compiler.frontend.unitree --> compiler.types.type_utils { Ability, Archetype, AtomTrailer, ElseIf, ElseStmt, Expr, HasVar, IfStmt, ImplDef, Import, KWPair, Module, ModuleItem, ModulePath, Name, Symbol, UnaryExpr, UniNode, UniScopeNode }
    compiler.frontend.unitree --> compiler.types.type_utils.expr_primitive_name { CfgExpr }
    type compiler.frontend.unitree --> compiler.types.types { Expr, Symbol, UniScopeNode as SymbolTable }
    compiler.frontend.unitree --> compiler.types.types.ClassType.get_class_symbol { Archetype }
    compiler.frontend.unitree --> compiler.types.types.ClassType.lookup_member_symbol { Ability, Archetype, Assignment, AtomTrailer, FuncSignature, ParamVar }
    compiler.frontend.unitree --> compiler.types.types._class_scope_category { Archetype }
    type compiler.frontend.unitree --> dist.native_product { Module }
    compiler.frontend.unitree --> dist.publish.dts { Ability, Archetype, AstTypedVarNode, FuncSignature, GlobalVars, Module, UniNode }
    compiler.frontend.unitree --> dist.publish.jsdoc { Ability, FuncSignature, Module, ParamVar, UniNode }
    compiler.frontend.unitree as uni --> lsp.server.engine;
    compiler.frontend.unitree --> lsp.server.engine { UniScopeNode }
    compiler.frontend.unitree --> lsp.server.engine.JacLangServer.type_check_file { Source as _Src }
    compiler.frontend.unitree as uni --> lsp.server.module_manager;
    compiler.frontend.unitree as uni --> lsp.server.sem_manager;
    compiler.frontend.unitree as uni --> lsp.server.utils;
    compiler.frontend.unitree --> lsp.server.utils { Symbol, UniScopeNode }
    compiler.frontend.codeinfo --> compiler.driver.wiring.WiringSpec.import_provider { is_bundled_native_module }
    compiler.frontend.codeinfo --> compiler.passes.ownership_check_pass.OwnershipCheckPass._nogc_resolve_provenance { NOGC_NATIVE_STDLIB, bundled_stdlib_module_of }
    compiler.frontend.diagnostics --> compiler.passes.import_wiring_pass { W2084 }
    compiler.frontend.codeinfo --> compiler.backends.native.kernel_stage0.running_kernel_target { KERNEL_UNIT_REL, jaclang_pkg_root }
    compiler.frontend.codeinfo --> compiler.backends.native.link_plan { JAC_ENTRY_SYMBOL }
    compiler.frontend.codeinfo --> compiler.backends.native.link_plan.LinkPlan.plan_digest | compiler.native_scope.package_host_edge { native_unit_identity }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass { NativeFuncLayout, is_package_keyed_path, native_unit_identity }
    compiler.frontend.codeinfo --> compiler.driver.boundary_classify.plain_native_import_target | compiler.driver.pass_driver._alert_in_internal_stub | compiler.driver.setup_progress | compiler.driver.source_failures._compiler_source_root | compiler.types.type_evaluator.TypeEvaluator.__post_init__ { jaclang_pkg_root }
    compiler.frontend.codeinfo --> compiler.driver.compilation_context { is_package_keyed_path }
    compiler.frontend.codeinfo --> compiler.driver.compiler.JacCompiler._wants_native_engine | compiler.driver.selfhost.SelfHostCache.owns | project.kernel_check.kernel_check | project.kernel_snapshot { is_compiler_source_path }
    compiler.frontend.codeinfo --> project.kernel_check.parity_mismatches { is_compiler_source_path }
    compiler.frontend.codeinfo --> compiler.driver.jir { is_package_keyed_path, native_unit_identity }
    compiler.frontend.codeinfo --> compiler.driver.native_iface { NATIVE_ABI_VERSION, NativeEnumLayout, NativeFieldInfo, NativeFuncLayout, NativeStructLayout, NativeTupleLayout, native_unit_identity, native_unit_root }
    compiler.frontend.codeinfo --> compiler.driver.program.JacProgram.declared_codespace { is_client_by_location }
    compiler.frontend.codeinfo --> compiler.driver.program.JacProgram.stamp_boundary_facts { is_bundled_native_module, resolve_native_module }
    compiler.frontend.codeinfo --> compiler.driver.session_compile.compile_in_session { get_effective_default_codespace_override, reset_native_unit_compile, set_effective_default_codespace, set_native_unit_compile }
    compiler.frontend.codeinfo --> compiler.driver.session_compile.inherit_session_options { set_effective_default_codespace }
    compiler.frontend.codeinfo --> compiler.erased_imports.erased_identity_call_arg { NATIVE_ERASED_IDENTITY_CALLS }
    compiler.frontend.codeinfo --> compiler.erased_imports.erased_import_binds { NATIVE_ERASED_IMPORTS }
    compiler.frontend.codeinfo --> compiler.passes.boundary_analysis_pass { InteropManifest }
    compiler.frontend.codeinfo --> dist.publish.runtime_vendor._runtime_module_options { is_native_by_location, is_shared_runtime_module }
    type compiler.frontend.codeinfo --> compiler.backends.py.codegen_shim | compiler.driver.progstate { CodeGenTarget }
    type compiler.frontend.codeinfo --> compiler.driver.boundary_classify { InteropManifest }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass { SymbolType }
    compiler.frontend.constant --> compiler.driver.program.JacProgram.parse_source | compiler.placement.placement_export { CodeContext }
    compiler.frontend.constant --> compiler.driver.program.JacProgram.stamp_boundary_facts { CodeContext }
    compiler.frontend.constant --> compiler.tools.cfg_dot.CoalesceBBPass._node_label { Tokens as Tok }
    compiler.frontend.constant --> compiler.types.builtin_extensions | compiler.types.stubcat.reader | compiler.types.type_evaluator | compiler.types.type_utils | compiler.types.types { ParamKind }
    compiler.frontend.diagnostics --> compiler.driver.program.JacProgram.module_scoped_errors { Category }
    compiler.frontend.diagnostics --> project.kernel_check.alert_of { DIAGNOSTICS }
    compiler.frontend.host --> compiler.backends.es.backends.registry.active_framework | compiler.backends.es.esast_gen_pass | compiler.backends.native.na_ir_gen_pass | compiler.backends.py.artifact_imports | compiler.driver.boundary_classify | compiler.driver.compilation_context.bind_options | compiler.driver.compile_options.CompileOptions.__post_init__ | compiler.driver.ifacecache.IfaceRegistry._entry_fresh | compiler.driver.module_analysis | compiler.driver.pipeline | compiler.driver.program.JacProgram._get_compiler | compiler.driver.progstate.DiagLedger._owned | compiler.driver.session_compile | compiler.driver.wiring | compiler.frontend.codeinfo.effective_default_codespace | compiler.frontend.helpers.evaluate_version_condition | compiler.frontend.parser.frontend.annex_paths | compiler.frontend.unitree.Import.__jac_detected.getter | compiler.passes.access_check_pass.AccessCheckPass._module_app_facts | compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass.enter_atom_trailer | compiler.passes.mtir_gen_pass.MTIRGenPass._get_scope_str | compiler.passes.ownership_check_pass.OwnershipCheckPass._nogc_module_enforced | compiler.passes.static_analysis_pass.StaticAnalysisPass._check_client_imports | compiler.passes.variant_agreement_pass.VariantAgreementPass._parse_sibling | compiler.placement.placement_facts | compiler.placement.placement_solver._native_dep_scan | compiler.symbol_utils.intrinsic_registry_if_ready | compiler.tools.jac_auto_lint_pass | compiler.types.type_evaluator.TypeEvaluator.__post_init__ | project.kernel_check { active_host }
    compiler.frontend.host --> compiler.driver.compilation_context.compilation_scope | compiler.driver.compile_options.CompileOptions.effective_triple | compiler.driver.ifacecache.IfaceRegistry.analysis_profile | compiler.driver.program.JacProgram.build | compiler.driver.progstate.ModuleHub.is_fresh | compiler.frontend.parser.frontend.annex_sources | compiler.frontend.unitree.Module.annexable_by.getter | compiler.passes.ownership_check_pass.OwnershipCheckPass._nogc_resolve_provenance | compiler.passes.static_analysis_pass.is_bootstrap_compiled_module | compiler.tools.jac_auto_lint_pass.JacAutoLintPass.__post_init__ | compiler.types.type_evaluator.TypeEvaluator._client_npm_base { active_host }
    compiler.frontend.host --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._opaque_field_if_unlowerable | compiler.driver.compilation_context.context_app | compiler.driver.program.JacProgram.compile | compiler.driver.progstate.ModuleHub.stamp | compiler.frontend.codeinfo.effective_native_target | compiler.frontend.parser.frontend.parse_woven | compiler.frontend.unitree.ModulePath.resolve_relative_path | compiler.tools.jac_auto_lint_pass.JacAutoLintPass._base_decl_archetypes | compiler.types.type_evaluator.TypeEvaluator._declared_missing_dependency { active_host }
    compiler.frontend.host --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._register_imported_archetype | compiler.driver.compilation_context.context_program | compiler.driver.program.JacProgram.execution_hubs | compiler.frontend.codeinfo.endpoint_descriptor | compiler.types.type_evaluator.TypeEvaluator._jac_virtual_sibling_dts { active_host }
    compiler.frontend.host --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._seam_warnings_on | compiler.driver.program.JacProgram.iface_registry | compiler.frontend.codeinfo.native_target_arch | compiler.types.type_evaluator.TypeEvaluator._load_ts_declarations { active_host }
    compiler.frontend.host --> compiler.driver.program.JacProgram.invalidate_module | compiler.frontend.codeinfo.resolve_native_module | compiler.types.type_evaluator.TypeEvaluator._resolve_client_npm_module { active_host }
    compiler.frontend.host --> compiler.driver.program.JacProgram.jac_file_formatter | compiler.types.type_evaluator.TypeEvaluator._resolve_submodule_attr { active_host }
    compiler.frontend.host --> compiler.driver.program.JacProgram.jac_file_linter | compiler.types.type_evaluator.TypeEvaluator._ts_decl_path { active_host }
    compiler.frontend.host --> compiler.driver.program.JacProgram.jac_str_formatter | compiler.types.type_evaluator.TypeEvaluator._untyped_external_is_error { active_host }
    compiler.frontend.host --> compiler.driver.program.JacProgram.load_dependency_module | compiler.types.type_evaluator.TypeEvaluator.get_type_of_module { active_host }
    compiler.frontend.host --> compiler.driver.program.JacProgram.native_units | compiler.types.type_evaluator.TypeEvaluator.get_type_of_module_item { active_host }
    compiler.frontend.host --> compiler.driver.program.JacProgram.note_stub_tree_served { active_host }
    compiler.frontend.host --> compiler.driver.program.JacProgram.parse_source { active_host }
    compiler.frontend.host --> compiler.driver.program.JacProgram.release_compile_closure { active_host }
    compiler.frontend.host --> compiler.driver.program.JacProgram.stamp_access_check_facts { active_host }
    compiler.frontend.host --> compiler.driver.program.JacProgram.stamp_app_facts { active_host }
    compiler.frontend.host --> compiler.driver.program.JacProgram.stub_catalog { active_host }
    compiler.frontend.host --> compiler.driver.compiler.JacCompiler.enter_compile { active_host, install_host }
    compiler.frontend.host --> compiler.driver.compiler.JacCompiler.finish_compile { install_host }
    compiler.frontend.host --> compiler.driver.pass_driver { CheckSettings, active_host }
    compiler.frontend.host --> compiler.frontend.codeinfo.jaclang_pkg_root | compiler.kernel_target.target_pkg_root { package_root }
    compiler.frontend.host --> compiler.frontend.kernel_analyze { active_host, install_host, set_package_root }
    compiler.frontend.host --> compiler.frontend.kernel_host { CheckSettings, HostPlatform, HostServices, LintSettings, PathFacts, ProjectDefaults, ProjectFacts, active_host, install_host }
    compiler.frontend.host --> compiler.frontend.kernel_inputs { CheckSettings, HostPlatform, LintSettings, ProjectDefaults, ProjectFacts }
    compiler.frontend.host --> compiler.frontend.source_layout { PathFacts }
    compiler.frontend.host --> compiler.placement.placement_pins { active_host }
    compiler.frontend.host --> project.compiler_host { CheckSettings, HostPlatform, HostServices, LintSettings, PathFacts, ProjectDefaults, ProjectFacts }
    compiler.frontend.host --> project.compiler_host.ProjectHost.native_analyze { active_host, install_host, kernel_host_enabled }
    compiler.frontend.host --> project.kernel_snapshot { HostServices, active_host, install_host, kernel_host_mode }
    type compiler.frontend.host --> compiler.driver.compiler { HostServices }
    compiler.frontend.kernel_analyze --> compiler.jc_unit { ANALYSIS_CRASHED, AnalysisReport, run_kernel_analysis }
    compiler.frontend.kernel_analyze --> project.kernel_check { AnalysisDiag, AnalysisReport, DiagSpan }
    compiler.frontend.kernel_analyze --> project.kernel_snapshot { ANALYSIS_CRASHED, ANALYSIS_OK, AnalysisReport, analysis_report, run_kernel_analysis }
    compiler.frontend.kernel_host --> compiler.frontend.kernel_analyze | project.compiler_host.ProjectHost.native_analyze { KernelHost }
    compiler.frontend.kernel_host --> project.kernel_snapshot { HostCensus, KernelHost }
    compiler.frontend.kernel_inputs --> compiler.frontend.kernel_analyze { KernelInputs, json_int, json_map, json_maps, json_opt_str, json_str_list }
    compiler.frontend.kernel_inputs --> compiler.frontend.kernel_host { DeclaredDependencies, ImportResolution, KEY_SEP, KernelInputs, LocalResolution, NpmAnswer, PythonInterface, local_key, pair_key, resolution_key }
    compiler.frontend.kernel_inputs --> project.kernel_snapshot { KernelInputs, ManifestSets, PythonInterface, request_of }
    type compiler.frontend.kernel_inputs --> project.compiler_host { KernelInputs }
    compiler.frontend.module_facts --> compiler.driver.program.JacProgram.stamp_native_import_facts | compiler.frontend.kernel_analyze { ModuleFacts }
    compiler.frontend.roles --> compiler.frontend.unparse | compiler.passes.annex_weave | compiler.tools.cfg_dot { Kid }
    compiler.frontend.roles --> compiler.passes.ownership_check_pass | compiler.passes.static_analysis_pass { BodyRole }
    compiler.frontend.roles --> compiler.tools.jac_formatter_pass { BodyRole, Kid }
    compiler.frontend.source_layout --> compiler.driver.bccache { LayoutTables, annex_files_of, base_file_of }
    compiler.frontend.source_layout --> compiler.frontend.kernel_host { annex_files_of, base_file_of, is_annex_path_of, list_directory, package_init_of, path_facts_of }
    compiler.frontend.source_layout --> compiler.frontend.kernel_inputs { LayoutTables }
    compiler.frontend.source_layout --> project.compiler_host.ProjectHost.is_annex_path_of { is_annex_path_of }
    compiler.frontend.source_layout --> project.compiler_host.ProjectHost.package_init { package_init_of }
    compiler.frontend.source_layout --> project.compiler_host.ProjectHost.path_facts { path_facts_of }
    compiler.frontend.srcloc --> compiler.frontend.kernel_analyze | project.kernel_check { Span }
    compiler.frontend.srcloc --> project.textio.span_for_file { Span as SrcSpan }
    type compiler.frontend.srcloc --> project.textio { Span }
    compiler.frontend.unitree as uni --> compiler.driver.module_analysis | compiler.driver.session_compile | compiler.frontend.unparse | compiler.placement.placement_export | project.compiler_host.ProjectHost.parse_python | project.kernel_snapshot;
    compiler.frontend.unitree --> compiler.backends.py.jcir_gen_pass { AstAccessNode }
    compiler.frontend.unitree --> compiler.driver.module_analysis | compiler.passes.execution { Module }
    compiler.frontend.unitree --> compiler.driver.pass_driver { Module, Source }
    compiler.frontend.unitree --> compiler.driver.pipeline_runner.compile_application { Import, ModulePath }
    compiler.frontend.unitree --> compiler.driver.program.JacProgram.resolve_absorb_imports { find_python_scope_node_of }
    compiler.frontend.unitree --> compiler.driver.program.JacProgram.stamp_boundary_facts { ability_of_symbol }
    compiler.frontend.unitree --> compiler.erased_imports { Ability, Expr, FuncCall, ImplDef, Import, Module, ModuleItem, Name, UniNode }
    compiler.frontend.unitree --> compiler.frontend.const_fold { Token }
    compiler.frontend.unitree --> compiler.frontend.kernel_host { Module, UniScopeNode }
    compiler.frontend.unitree --> compiler.passes.annex_weave { EmptyToken, Import, ModuleItem, ModulePath, UniNode }
    compiler.frontend.unitree --> compiler.passes.context { Module, TreeWalker }
    compiler.frontend.unitree --> compiler.passes.endpoint_effect_pass { Expr, ListVal, MultiString, String }
    compiler.frontend.unitree --> compiler.passes.layout_pass { KWPair, Token, UniScopeNode }
    compiler.frontend.unitree --> compiler.passes.wasm_contract { Expr, FuncCall, Module }
    compiler.frontend.unitree --> compiler.symbol_utils { ImplDef }
    compiler.frontend.unitree --> compiler.tools.cfg_dot { Ability, Archetype, AssertStmt, AstElseBodyNode, AtomUnit, AwaitingClause, BoolExpr, CfgExpr, CodeBlockStmt, CtrlStmt, DictCompr, DisengageStmt, ElseIf, ElseStmt, Except, Expr, FinallyStmt, ForeverStmt, GenCompr, GlobalVars, IfElseExpr, IfStmt, ImplDef, InForStmt, InnerCompr, IterForStmt, JsxSlot, LambdaExpr, ListCompr, MatchCase, MatchStmt, Module, ModuleCode, Name, OpenStmt, RaiseStmt, ReturnStmt, SemDef, Semi, SetCompr, SwitchCase, SwitchStmt, Test, Token, TreeWalker, TryStmt, TypeAlias, TypedCtxBlock, UniCFGNode, UniNode, WhileStmt, WithStmt }
    compiler.frontend.unitree --> compiler.types.ct_eval { AstImplNeedingNode, UniScopeNode }
    type compiler.frontend.unitree --> compiler.driver.ifacecache | compiler.frontend.host | compiler.types.stubcat.resolver | project.compiler_host { Module }
    type compiler.frontend.unitree --> compiler.frontend.codeinfo { Module, UniNode }
    compiler.frontend.unparse --> compiler.backends.es.esast_gen_pass | compiler.backends.native.na_ir_gen_pass.NaIRGenPass._emit_unlowerable_type | compiler.passes.endpoint_effect_pass.EndpointEffectPass._scan | compiler.passes.layout_pass | compiler.passes.mtir_gen_pass | compiler.passes.variant_agreement_pass.annotation_text | compiler.passes.wasm_contract.value_contract | compiler.tools.cfg_dot.CoalesceBBPass._node_label | compiler.tools.code_intel | compiler.tools.jac_auto_lint_pass | dist.publish.dts | dist.publish.jsdoc | lsp.server.engine { unparse_node }
    compiler.frontend.codeinfo --> dist.precompile_bytecode.is_toolchain_package { jaclang_pkg_root }
    compiler.frontend.codeinfo --> compiler.driver.wiring.compiled_by_seed { jaclang_pkg_root }
    compiler.frontend.codeinfo --> compiler.driver.wiring.is_kernel_abi_contract { jaclang_pkg_root }
    compiler.frontend.codeinfo --> compiler.driver.wiring.is_native_stdlib_source { jaclang_pkg_root }
    compiler.frontend.host --> compiler.driver.wiring { HOST_FACT_GIT_IGNORED, HOST_FACT_SEP, HOST_FACT_STDLIB_MODULES }
    compiler.frontend.codeinfo --> dist.precompile_bytecode._compiler_kernel_units { kernel_unit_paths }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._demote_native_test { native_test_symbol }
    compiler.frontend.codeinfo --> compiler.types.stubcat.build._cached_catalog { jaclang_pkg_root }
    compiler.frontend.codeinfo --> compiler.driver.jir | compiler.passes.package_boundary_pass.PackageBoundaryPass.run_walk { is_compiler_source_path }
    compiler.frontend.codeinfo --> compiler.driver.jir.native_producer_digest { NATIVE_ABI_VERSION }
    compiler.frontend.constant --> packages.api { SymbolAccess, SymbolType }
    compiler.frontend.diagnostics --> compiler.passes.package_boundary_pass { E2095, E2096 }
    compiler.frontend.host --> compiler.passes.package_boundary_pass { ProjectFacts, active_host }
    compiler.frontend.host --> compiler.types.ct_eval.CtEvaluator._embed { active_host }
    compiler.frontend.module_facts --> compiler.driver.boundary_classify.python_side_name_refs | compiler.passes.package_boundary_pass { ModuleFacts }
    compiler.frontend.unitree --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._record_generic_definition | compiler.types.ct_eval { definition_qualname }
    compiler.frontend.unitree --> compiler.passes.layout_pass { GlobalVars, ParamVar }
    compiler.frontend.unitree --> compiler.passes.package_boundary_pass { Import, Module, ModulePath }
    compiler.frontend.unitree --> packages.api { HasVar, Module, Symbol }
    compiler.frontend.codeinfo --> compiler.backends.es.esast_gen_pass { InteropManifest }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._from_imported_intercept { bundled_stdlib_module_of }
    compiler.frontend.codeinfo --> compiler.driver.compiler { ClientArtifact, ClientManifest }
    compiler.frontend.codeinfo --> compiler.driver.unit_products { ClientArtifact, ClientManifest, InteropBinding, InteropContext, InteropManifest }
    compiler.frontend.codeinfo --> compiler.native_compiler.NativeCompiler._resolve_classes { NATIVE_ARCH_SCOPE_SEP }
    compiler.frontend.codeinfo --> compiler.passes.layout_pass.interface_class_native_name { native_arch_name }
    compiler.frontend.codeinfo --> compiler.placement.placement_solver._import_source_module { is_compiler_source_path }
    compiler.frontend.codeinfo --> project.compiler_host.ProjectHost.client_stub_globals { jaclang_pkg_root }
    compiler.frontend.codeinfo --> project.kernel_compile.kernel_route { is_compiler_source_path }
    compiler.frontend.codeinfo --> project.kernel_snapshot.native_stdlib_misses { native_stdlib_root }
    compiler.frontend.constant --> compiler.driver.module_compile { CodeContext }
    compiler.frontend.constant --> compiler.driver.unit_products { CodeContext }
    compiler.frontend.diagnostics --> compiler.driver.module_compile.report_missing_native_ir { E5092 }
    compiler.frontend.diagnostics --> compiler.passes.ast_validation_pass { E2036 }
    compiler.frontend.host --> compiler.backends.es.free_ident_audit.client_ambient_globals { active_host }
    compiler.frontend.host --> compiler.backends.es.jac_runtime_js.build_osp_core_js { active_host }
    compiler.frontend.host --> compiler.driver.application._kernel_units { active_host }
    compiler.frontend.host --> compiler.driver.compiler.JacCompiler._adopt_kernel_compile { active_host }
    compiler.frontend.host --> compiler.driver.jir.stored_wiring_digest { active_host }
    compiler.frontend.host --> compiler.driver.module_compile { active_host }
    compiler.frontend.host --> compiler.driver.unit_products.dependency_span_rows { active_host }
    compiler.frontend.host --> compiler.placement.placement_solver._held_pull_ids { active_host }
    compiler.frontend.host --> compiler.placement.placement_solver._pull_into_target { active_host }
    compiler.frontend.host --> project.kernel_compile { HostServices }
    compiler.frontend.host --> project.kernel_snapshot.session_inputs { package_root }
    type compiler.frontend.kernel_analyze --> compiler.frontend.host { CompileReport }
    type compiler.frontend.kernel_analyze --> compiler.frontend.kernel_host { CompileReport }
    compiler.frontend.kernel_analyze --> compiler.jc_unit { CompileReport, run_kernel_compile }
    type compiler.frontend.kernel_analyze --> project.compiler_host { CompileReport }
    compiler.frontend.kernel_analyze --> project.kernel_compile { ANALYSIS_CRASHED, AnalysisReport, CompileReport, ModuleReport, kernel_trace, run_kernel_compile }
    compiler.frontend.kernel_host --> compiler.frontend.kernel_analyze { HostAsker }
    compiler.frontend.kernel_host --> project.kernel_snapshot { EMIT_QUESTION, HOST_ONLY_ANSWER, HostAsker }
    compiler.frontend.kernel_inputs --> compiler.driver.unit_products.client_artifact_from_json { json_map, json_str_list, json_str_map }
    compiler.frontend.kernel_inputs --> compiler.driver.unit_products.literal_from_json { json_map }
    compiler.frontend.kernel_inputs --> compiler.driver.unit_products.manifest_from_record { json_map, json_maps, json_opt_str, json_str_list, json_str_map }
    compiler.frontend.kernel_inputs --> compiler.driver.unit_products.products_from_record { json_str_list }
    compiler.frontend.kernel_inputs --> compiler.driver.unit_products.str_list_map { json_map, json_str_list }
    compiler.frontend.kernel_inputs --> compiler.frontend.kernel_host { json_map, merge_answers }
    compiler.frontend.kernel_inputs --> project.kernel_snapshot { KEY_SEP, NpmAnswer, answers_to_dict, pair_key }
    compiler.frontend.module_facts --> compiler.driver.module_compile { ModuleFacts }
    compiler.frontend.source_layout --> compiler.backends.es.scoped_styles { style_annex_of }
    compiler.frontend.source_layout --> compiler.driver.jir._related_files { style_annex_of }
    compiler.frontend.unitree as uni --> compiler.backends.es.backends.react;
    compiler.frontend.unitree as uni --> compiler.backends.es.backends.solid;
    compiler.frontend.unitree as uni --> compiler.driver.module_compile;
    compiler.frontend.unitree as uni --> compiler.driver.unit_products;
    compiler.frontend.unitree --> compiler.passes.type_checker_pass { MatchArch }
    compiler.frontend.codeinfo --> cli.commands.native_build._application_ir { is_toolchain_unit }
    compiler.frontend.codeinfo --> client.js_runtime._pkg_dir { jaclang_pkg_root }
    compiler.frontend.codeinfo --> compiler.backends.native.floors._repo_root { jaclang_pkg_root }
    compiler.frontend.codeinfo --> compiler.backends.native.kernel_resolve._unit_label { jaclang_pkg_root }
    compiler.frontend.codeinfo --> compiler.backends.native.kernel_resolve.unit_drift { native_unit_identity }
    compiler.frontend.codeinfo --> compiler.backends.native.llvm.shim_path._repo_root { jaclang_pkg_root }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._default_repr_fn { native_safe_sym }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._final_variant_value { native_variant_of }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._forward_declare_imported_ability { NativeModuleLayout }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._maybe_declare_ability { NativeModuleLayout }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._native_variant_decl { native_variant_of }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._place_unit_python { native_display_text }
    compiler.frontend.codeinfo --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._ret_tuple_hints { NativeTupleLayout }
    compiler.frontend.codeinfo --> compiler.driver.ifacecache.native_lowering_reads { is_compiler_source_path, is_native_by_location }
    compiler.frontend.codeinfo --> compiler.driver.jir._memoized { _native_target_ctx, get_effective_default_codespace_override }
    compiler.frontend.codeinfo --> compiler.driver.nativecache.NativeUnitRegistry.adopt_lowered { CodeGenTarget }
    compiler.frontend.codeinfo --> compiler.driver.nativecache.NativeUnitRegistry.note_step { native_unit_identity }
    compiler.frontend.codeinfo --> compiler.driver.program.JacProgram.prefers_native_codespace { is_kernel_unit_path }
    compiler.frontend.codeinfo --> compiler.driver.program.JacProgram.toolchain_dependency { is_compiler_source_path }
    compiler.frontend.codeinfo --> compiler.driver.session_compile.drop_native_bindings { InteropContext, InteropManifest }
    compiler.frontend.codeinfo --> compiler.frontend.host.HostServices.typeshed_unavailable_reason { jaclang_pkg_root }
    compiler.frontend.codeinfo --> compiler.frontend.kernel_host.KernelHost.compile_module { native_stdlib_root }
    compiler.frontend.codeinfo --> compiler.frontend.kernel_host.KernelHost.lower_dependency { get_effective_default_codespace_override, set_effective_default_codespace }
    compiler.frontend.codeinfo --> compiler.frontend.unitree.ModulePath.native_variant_path { _native_variant_path }
    compiler.frontend.codeinfo --> compiler.native_bindings.NativeBindings.surface { NATIVE_STDLIB_EXTENSIONS, NATIVE_SUPPORTED_STDLIB, is_bundled_native_module, resolve_native_module }
    compiler.frontend.codeinfo --> compiler.native_bindings.import_gaps { resolve_native_module }
    compiler.frontend.codeinfo --> compiler.native_bindings.typeshed_stub_path { jaclang_pkg_root }
    compiler.frontend.codeinfo --> compiler.native_scope.binds_bare_arch_names { kernel_unit_rels }
    compiler.frontend.codeinfo --> compiler.passes.layout_pass._archetype_native_name { native_arch_name }
    compiler.frontend.codeinfo --> compiler.passes.layout_pass._recorded_native_name { bundled_stdlib_module_of }
    compiler.frontend.codeinfo --> compiler.passes.layout_pass.archetype_native_name { bundled_stdlib_module_of }
    compiler.frontend.codeinfo --> compiler.passes.layout_pass.record_interface_twins { bundled_stdlib_module_of }
    compiler.frontend.codeinfo --> compiler.passes.ownership_check_pass.OwnershipCheckPass._nogc_resolve_provenance { is_toolchain_unit }
    compiler.frontend.codeinfo --> compiler.placement.placement.native_blocker_scan { NATIVE_SUPPORTED_STDLIB, is_bundled_native_module, resolve_native_module }
    compiler.frontend.codeinfo --> compiler.placement.placement_facts.variant_selected { is_native_variant_path, is_selected_native_variant }
    compiler.frontend.codeinfo --> compiler.placement.placement_solver.native_closure_blocker { native_unit_compile_active }
    compiler.frontend.codeinfo --> dist.interpreter._repo_root { jaclang_pkg_root }
    compiler.frontend.codeinfo --> dist.precompiled._pkg_dir { jaclang_pkg_root }
    compiler.frontend.codeinfo --> project.compiler_host.ProjectHost.held_native_iface { is_compiler_source_path }
    compiler.frontend.codeinfo --> server.watcher.watch_roots { is_compiler_source_path }
    compiler.frontend.const_fold --> compiler.backends.py.jcir_gen_pass { fold_const }
    compiler.frontend.const_fold --> compiler.c_interop.c_scalar_constant { fold_const }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._binds_variable { SymbolType }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._c_vararg { is_borrow_kind }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._c_vararg_value { is_borrow_kind }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._clib_abi_signature { is_borrow_kind }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._clib_param_borrowed { is_borrow_kind }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_assignment { SymbolStorage }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._null_safe_on_value { SymbolType }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._register_entry_globals { SymbolStorage }
    compiler.frontend.constant --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._unpack_into { SymbolStorage }
    compiler.frontend.constant --> compiler.c_interop.c_lent_arg_elem { is_borrow_kind }
    compiler.frontend.constant --> compiler.c_interop.c_lent_param { is_borrow_kind }
    compiler.frontend.constant --> compiler.driver.module_analysis.run_analysis { CodeContext as _CodeCtx }
    compiler.frontend.constant --> compiler.frontend.loop_links { ExprCtx, SymbolType }
    compiler.frontend.constant --> compiler.native_bindings { ParamKind, Tokens as Tok }
    compiler.frontend.constant --> compiler.passes.layout_pass.open_dispatch { SymbolAccess }
    compiler.frontend.constant --> compiler.passes.placement_pass { CodeContext }
    compiler.frontend.constant --> compiler.passes.static_analysis_pass { client_state_setter_name }
    compiler.frontend.constant --> compiler.passes.sym_tab_build_pass.SymTabBuildPass._declare_global_vars { SymbolType }
    compiler.frontend.constant --> compiler.passes.type_checker_pass.TypeCheckPass._borrowed_scalar_param { OwnershipKind }
    compiler.frontend.constant --> compiler.passes.type_checker_pass.TypeCheckPass._check_borrowed_scalar_forward { OwnershipKind, is_borrow_kind }
    compiler.frontend.constant --> compiler.passes.type_checker_pass.TypeCheckPass._check_c_function_def { is_borrow_kind }
    compiler.frontend.constant --> compiler.placement.placement_facts.settle_server { CodeContext }
    compiler.frontend.constant --> compiler.types.type_evaluator.TypeEvaluator._c_lent_args { is_borrow_kind }
    compiler.frontend.diagnostics --> compiler.backends.native.na_ir_gen_pass { E1145, E1158, E5113, E5114 }
    compiler.frontend.diagnostics --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass.finish { E5115 }
    compiler.frontend.diagnostics --> compiler.passes.placement_pass { DIAGNOSTICS, E5090, E5116 }
    compiler.frontend.diagnostics --> compiler.passes.placement_pass.PlacementPass._run_decided { E5096 }
    compiler.frontend.diagnostics --> compiler.passes.placement_pass.PlacementPass._run_undecided { E5096 }
    compiler.frontend.diagnostics --> compiler.passes.type_checker_pass { E1153, E1154, E1155, E1156, E1157, E1158, E1159 }
    compiler.frontend.host --> compiler.backends.native.abi.struct_layouts { active_host }
    compiler.frontend.host --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._place_unit_python { active_host }
    compiler.frontend.host --> compiler.driver.jir._memoized { active_host }
    compiler.frontend.host --> compiler.driver.jir._project_env_fingerprint_uncached { active_host }
    compiler.frontend.host --> compiler.driver.native_iface.resolve_native_unit_ref { active_host }
    compiler.frontend.host --> compiler.driver.nativecache.NativeUnitRegistry.adopt_lowered { active_host }
    compiler.frontend.host --> compiler.native_scope.binds_bare_arch_names { active_host }
    compiler.frontend.host --> compiler.passes.placement_pass.PlacementPass._run_decided { active_host }
    compiler.frontend.host --> compiler.passes.placement_pass.PlacementPass._run_undecided { active_host }
    compiler.frontend.host --> compiler.passes.placement_pass.settle_native_module { active_host }
    compiler.frontend.host --> compiler.placement.placement_solver.native_placement_candidate { active_host }
    compiler.frontend.kernel_host --> project.kernel_compile.kernel_compile_reported { replay_event_rows }
    compiler.frontend.loop_links --> compiler.backends.es.esast_gen_pass { LoopLinks, LoopStmt, PassLink, assigned_on_entry, binding_sites, binds_target, confined_to, enclosing_loop, is_within }
    compiler.frontend.loop_links --> compiler.backends.native.na_ir_gen_pass { LoopLinks, LoopStmt, PassLink, enclosing_loop, frame_owns }
    compiler.frontend.loop_links --> compiler.backends.py.jcir_gen_pass { LoopLinks, LoopStmt, PassLink }
    compiler.frontend.module_facts --> compiler.native_bindings { ModuleFacts }
    compiler.frontend.module_facts --> compiler.passes.layout_pass { ModuleFacts }
    compiler.frontend.module_facts --> compiler.passes.placement_pass { ModuleFacts }
    compiler.frontend.module_facts --> compiler.passes.placement_pass.client_refused_elements { client_capability_violations }
    compiler.frontend.relations --> compiler.frontend.unitree { CalleeSignature }
    compiler.frontend.unitree --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._binds_variable { ability_of_symbol }
    compiler.frontend.unitree --> compiler.boundary_rules { Ability, Archetype, Assignment, AtomTrailer, AtomUnit, BinaryExpr, Ellipsis, Enum, FuncSignature, HasVar, IndexSlice, Module, MultiString, NameAtom, Null, String, Token, TupleVal, TypeAlias, UniNode, resolved_decl_of }
    compiler.frontend.unitree --> compiler.c_interop { Ability, GlobalVars, Name, ParamVar, Symbol, resolved_decl_of }
    compiler.frontend.unitree --> compiler.c_interop._ambient_c_call_returns { FuncCall, Name }
    compiler.frontend.unitree --> compiler.c_interop._fold_with_finals { BinaryExpr }
    compiler.frontend.unitree --> compiler.c_interop._spelled_c_type_name { Name }
    compiler.frontend.unitree --> compiler.c_interop.c_abi_callee { FuncCall }
    compiler.frontend.unitree --> compiler.c_interop.c_bytes_array_definition { MultiString, String }
    compiler.frontend.unitree --> compiler.c_interop.c_bytes_literal { MultiString, String }
    compiler.frontend.unitree --> compiler.c_interop.c_lent_param { FuncCall, FuncSignature, KWPair }
    compiler.frontend.unitree --> compiler.c_interop.c_param_type { FuncCall }
    compiler.frontend.unitree --> compiler.c_interop.c_scalar_constant { BinaryExpr, FuncCall, Name }
    compiler.frontend.unitree --> compiler.c_interop.c_string_literal { FString, MultiString, literal_string_value }
    compiler.frontend.unitree --> compiler.c_interop.c_variadic_param { FuncSignature }
    compiler.frontend.unitree --> compiler.c_interop.clib_block_defines { Ability }
    compiler.frontend.unitree --> compiler.c_interop.clib_global_of_name { Ability, ImplDef, LambdaExpr, Module, Test }
    compiler.frontend.unitree --> compiler.c_interop.final_glob_value { Name }
    compiler.frontend.unitree --> compiler.c_interop.named_function_of { Ability, Name }
    compiler.frontend.unitree --> compiler.capability_notes { Module, UniNode }
    compiler.frontend.unitree --> compiler.frontend.loop_links { Ability, Archetype, Assignment, CtrlStmt, DictCompr, Enum, ForeverStmt, ImplDef, InForStmt, InnerCompr, IterForStmt, LambdaExpr, ListCompr, Module, ModuleCode, Name, Symbol, Test, UniNode, UniScopeNode, WhileStmt, is_identifier_slot, same_lexical_scope }
    compiler.frontend.unitree --> compiler.native_bindings { Ability, Archetype, AtomTrailer, Enum, FuncCall, FuncSignature, GlobalVars, HasVar, Import, KWPair, Module, ModuleItem, Name, Symbol, TypeAlias, UniNode, UniScopeNode, resolved_decl_of }
    compiler.frontend.unitree --> compiler.passes.boundary_analysis_pass { ContextAwareNode }
    compiler.frontend.unitree --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._route_facts { KWPair }
    compiler.frontend.unitree --> compiler.passes.boundary_analysis_pass.route_literal { Null }
    compiler.frontend.unitree --> compiler.passes.placement_pass { Ability, Archetype, AtomTrailer, ContextAwareNode, ImplDef, Import, Module, ModuleCode, ModuleItem, ModulePath, Name, Test, UniNode }
    compiler.frontend.unitree --> compiler.passes.static_analysis_pass { HasVar, JsxElement, JsxElementName }
    compiler.frontend.unitree --> compiler.passes.static_analysis_pass.StaticAnalysisPass._check_undefined_names { JsxElementName }
    compiler.frontend.unitree --> compiler.passes.type_checker_pass { AtomUnit, GlobalVars, String }
    compiler.frontend.unparse --> compiler.boundary_rules.json_refusal { unparse_node }
    compiler.frontend.unparse --> compiler.boundary_rules.signature_refusals { unparse_node }
    compiler.frontend.codeinfo --> cli.commands.execution._count_jac_files { is_compiler_source_path }
    compiler.frontend.codeinfo --> server.watcher.JacFileWatcher._on_change { is_compiler_source_path }
    compiler.frontend.codeinfo --> compiler.passes.endpoint_effect_pass.EndpointEffectPass.record_callables { is_compiler_source_path }
    compiler.frontend.kernel_inputs --> compiler.driver.application._reusable_interfaces { PythonInterface }
    compiler.frontend.kernel_inputs --> project.kernel_compile { PythonInterface }
    compiler.frontend.unitree --> compiler.passes.endpoint_effect_pass { UniScopeNode }
    compiler.frontend.unparse --> compiler.passes.endpoint_effect_pass.EndpointEffectPass._apply { unparse_node }
    compiler.frontend.parser.frontend --> cli.commands.analysis._check_file_job { _replay_diags, parse_diags }
    compiler.frontend.parser.frontend --> cli.commands.architecture._parse_imports { parse_woven }
    compiler.frontend.parser.frontend --> compiler.driver.wiring.parse_records { parse_woven }
    compiler.frontend.parser.frontend --> compiler.passes.variant_agreement_pass.VariantAgreementPass._parse_sibling { parse }
    compiler.frontend.parser.frontend --> compiler.tests.test_module_exports { parse }
    compiler.frontend.parser.frontend --> lsp.server.engine.JacLangServer.type_check_file { _replay_diags, parse_diags }
    compiler.frontend.parser.lexer --> cli.commands.analysis._check_file_job { Lexer }
    compiler.frontend.parser.lexer --> cli.commands.fix._strip_markers { tokenize }
    compiler.frontend.parser.lexer as na_lexer --> compiler.frontend.parser.frontend;
    compiler.frontend.parser.lexer --> compiler.frontend.parser.frontend { Lexer }
    compiler.frontend.parser.lexer --> compiler.frontend.parser.parser { tokenize_full }
    compiler.frontend.parser.lexer --> lsp.server.engine { tokenize_full }
    compiler.frontend.parser.lexer --> lsp.server.engine.JacLangServer.type_check_file { Lexer as _Lexer }
    compiler.frontend.parser.parser --> cli.commands.analysis._check_file_job { Parser as _SyntaxParser }
    compiler.frontend.parser.parser --> compiler.frontend.parser.frontend { Parser, parse_expression as _parse_expression }
    compiler.frontend.parser.parser --> compiler.jc_unit { parse_program }
    compiler.frontend.parser.parser --> compiler.types.type_evaluator.TypeEvaluator._resolve_string_type_expr { parse_expression }
    compiler.frontend.parser.parser --> lsp.server.engine.JacLangServer.type_check_file { Parser as _SyntaxParser }
    compiler.frontend.parser.tokens --> cli.commands.fix { LexToken }
    compiler.frontend.parser.tokens --> compiler.frontend.parser.frontend { CommentData, SrcDiag }
    compiler.frontend.parser.tokens --> compiler.frontend.parser.lexer { CommentData, LexToken, SourceLoc, SrcDiag, TokenKind, is_special_var_kind, lookup_keyword }
    compiler.frontend.parser.tokens --> compiler.frontend.parser.parser { CommentData, LexToken, SourceLoc, SrcDiag, TokenKind, is_builtin_type_kind, is_reserved_kind, is_special_var_kind }
    compiler.frontend.parser.tokens --> compiler.jc_unit { CommentData, SrcDiag }
    type compiler.frontend.parser.tokens --> compiler.native_compiler { CommentData, SrcDiag }
    compiler.frontend.parser.tokens --> compiler.tools.grammar_extract_pass { BUILTIN_TYPE_KINDS, TokenKind }
    compiler.frontend.parser.tokens --> compiler.tools.jac_auto_lint_pass { KEYWORDS }
    compiler.frontend.parser.tokens --> lsp.server.engine { TokenKind }
    compiler.frontend.parser.frontend --> compiler.driver.program.JacProgram.parse_source { annex_sources, parse_woven }
    compiler.frontend.parser.frontend --> compiler.tools.jac_auto_lint_pass.JacAutoLintPass._base_decl_archetypes { parse as rd_parse }
    compiler.frontend.parser.frontend --> project.compiler_host.ProjectHost.native_parse { finish_parse }
    compiler.frontend.parser.lexer --> compiler.tools.jac_auto_lint_pass.JacAutoLintPass._reparse_signature { tokenize_full }
    compiler.frontend.parser.parser --> compiler.tools.jac_auto_lint_pass.JacAutoLintPass._reparse_signature { Parser }
    compiler.frontend.parser.frontend --> compiler.placement.placement_solver._native_dep_scan { parse as rd_parse }
    compiler.frontend.parser.frontend --> project.compiler_host.ProjectHost.woven_module { annex_sources, parse_woven }
    compiler.frontend.parser.frontend --> compiler.driver.nativecache._module_files_and_imports { parse as rd_parse }
    compiler.passes.annex_weave --> compiler.frontend.parser.frontend.parse_woven { merge_annex_into }
    compiler.passes.ast_validation_pass --> compiler.driver.pipeline { ASTValidationPass }
    compiler.passes.boundary_analysis_pass --> compiler.driver.pipeline { BoundaryAnalysisPass }
    compiler.passes.capability_check_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._fstring_spec_text { static_fstring_spec_text }
    compiler.passes.capability_check_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._process_clib_imports { classify_native_import }
    compiler.passes.cfg_build_pass --> compiler.tests.test_pipeline_products { CFGBuildPass }
    type compiler.passes.context --> client.client_diagnostics { Alert }
    compiler.passes.context --> compiler.backends.native.na_compile_pass { CompileContext }
    compiler.passes.context --> compiler.backends.native.na_ir_gen_pass { CompileContext }
    compiler.passes.context --> compiler.backends.py.jcir_bc_gen_pass { CompileContext }
    compiler.passes.context --> compiler.driver.context_passes { CompileContext }
    compiler.passes.context --> compiler.driver.ifacecache._alert_from_record { Alert }
    compiler.passes.context --> compiler.driver.pass_driver { Alert, DiagnosticPolicy }
    compiler.passes.context --> compiler.driver.program { Alert }
    compiler.passes.context --> compiler.driver.progstate { Alert, PassResult }
    compiler.passes.context --> compiler.frontend.parser.frontend { Alert }
    compiler.passes.context --> compiler.jc_unit { Alert, CompileContext }
    type compiler.passes.context --> compiler.native_compiler { Alert, PassResult }
    compiler.passes.context --> compiler.native_compiler.NativeCompiler.take_pass_results { PassResult as CompletedPassResult }
    compiler.passes.context --> compiler.passes.access_check_pass { CompileContext }
    compiler.passes.context --> compiler.passes.ast_validation_pass { CompileContext }
    compiler.passes.context --> compiler.passes.boundary_analysis_pass { CompileContext }
    compiler.passes.context --> compiler.passes.capability_check_pass { CompileContext }
    compiler.passes.context --> compiler.passes.cfg_build_pass { CompileContext }
    compiler.passes.context --> compiler.passes.decl_impl_match_pass { CompileContext }
    compiler.passes.context --> compiler.passes.endpoint_effect_pass { CompileContext }
    compiler.passes.context --> compiler.passes.execution { Alert, CompileContext, DiagnosticPolicy, PassResult }
    compiler.passes.context --> compiler.passes.freeze_structure_pass { CompileContext }
    compiler.passes.context --> compiler.passes.graph_lowering_pass { CompileContext }
    compiler.passes.context --> compiler.passes.import_wiring_pass { CompileContext }
    compiler.passes.context --> compiler.passes.jsx_intrinsic_guard_pass { CompileContext }
    compiler.passes.context --> compiler.passes.layout_pass { CompileContext }
    compiler.passes.context --> compiler.passes.mtir_gen_pass { CompileContext }
    compiler.passes.context --> compiler.passes.ownership_check_pass { CompileContext }
    compiler.passes.context --> compiler.passes.pyast_load_pass { CompileContext }
    compiler.passes.context --> compiler.passes.rc_facts_pass { CompileContext }
    compiler.passes.context --> compiler.passes.region_infer_pass { CompileContext }
    compiler.passes.context --> compiler.passes.sem_def_match_pass { CompileContext }
    compiler.passes.context --> compiler.passes.semantic_analysis_pass { CompileContext }
    compiler.passes.context --> compiler.passes.static_analysis_pass { CompileContext }
    compiler.passes.context --> compiler.passes.sym_tab_build_pass { CompileContext }
    compiler.passes.context --> compiler.passes.type_checker_pass { CompileContext }
    compiler.passes.context --> compiler.passes.variant_agreement_pass { CompileContext }
    compiler.passes.context --> compiler.placement.placement_solver._emit_solver_warning { Alert }
    compiler.passes.context --> compiler.tools.comment_attach_pass { CompileContext }
    compiler.passes.context --> compiler.tools.doc_ir_gen_pass { CompileContext }
    compiler.passes.context --> compiler.tools.grammar_extract_pass { CompileContext }
    compiler.passes.context --> compiler.tools.jac_auto_lint_pass { CompileContext }
    compiler.passes.context --> compiler.tools.jac_formatter_pass { CompileContext }
    compiler.passes.context --> compiler.tools.normalize_pass { CompileContext }
    compiler.passes.context --> compiler.tools.unparse_pass { CompileContext }
    compiler.passes.context --> compiler.types.type_evaluator { CompileContext }
    type compiler.passes.context --> lsp.server.engine { Alert }
    compiler.passes.context --> lsp.server.utils { Alert }
    type compiler.passes.context --> server.hmr { Alert }
    compiler.passes.dataflow --> compiler.passes.ownership_check_pass { solve_backward, solve_forward, solve_forward_must }
    compiler.passes.dataflow --> compiler.passes.rc_facts_pass { solve_backward_gen_kill }
    compiler.passes.decl_impl_match_pass --> compiler.driver.pipeline { DeclImplMatchPass }
    compiler.passes.endpoint_effect_pass --> compiler.driver.pipeline { EndpointEffectPass }
    compiler.passes.execution --> compiler.driver.pass_driver { run_walker }
    compiler.passes.execution --> compiler.tests.xbackend_equiv { run_walker }
    compiler.passes.graph_lowering_pass --> compiler.driver.pipeline { GraphLoweringPass }
    compiler.passes.import_wiring_pass --> compiler.driver.pipeline { ImportWiringPass }
    compiler.passes.layout_pass --> compiler.backends.es.esast_gen_pass.EsastGenPass._field_constructor_args { archetype_native_name, get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass { ACCESSOR_SLOT_SUFFIX, ArchetypeLayout, EnumLayout, VTABLE_HEADER_SLOTS, accessor_slot_name, archetype_accessors, native_type_key }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._aos_elem_name { class_type_native_name }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._arch_is_acyclic { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._arch_is_osp_name { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._arch_is_walker_name { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._arch_key { archetype_native_name }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._arch_layout { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._arch_ref_key { referenced_native_name }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._class_const_declarer { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._class_const_variants { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_archetype { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_class_form_enum_member { class_form_enum_member }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_enum_layout { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_instantiation { get_layout_registry as _ci_glr }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_virtual_call { get_layout_registry as _vc_glr, get_layout_registry as _vd_glr }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._elem_arch_name_of { class_type_native_name }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._emit_dispatched_field_ptr { get_layout_registry as _df_glr }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._emit_isa_hashed_fn { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._ensure_enum_lowered { class_form_enum_scalar, enum_decl_of, enum_value_type_of, is_enum_class_type }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._enum_ctor_layout { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._is_enum_arch { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._isinstance_needs_class_name { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._isinstance_unprovable_class { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._jc_reference_schema { class_type_native_name }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._lower_class_type { class_type_native_name }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._mangled_of { native_type_key }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._mro_of { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._native_archetypes { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._nogc_osp_skip { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._nogc_type_arg_mangles { native_type_key }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._osp_edge_class_name { class_type_native_name }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._receiver_routed_method_fn { get_layout_registry as _sc_glr }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._register_archetypes { get_layout_registry, get_layout_registry as _no_glr }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._register_class_consts { class_form_enum_scalar }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._register_imported_hierarchy { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._register_imported_struct_types { adopt_imported_bases }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._resolve_method { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._resolve_method_owner { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._visit_nonprimary_ancestor_methods { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._vtable_candidates { get_layout_registry }
    compiler.passes.layout_pass --> compiler.passes.osp_analysis.OspAnalysis._isa_closure { referenced_native_name }
    compiler.passes.layout_pass --> compiler.passes.osp_analysis.OspAnalysis.arch_key { archetype_native_name }
    compiler.passes.layout_pass --> compiler.passes.osp_analysis.OspAnalysis.native_slot_triggers { native_type_key, referenced_native_name }
    compiler.passes.layout_pass --> compiler.symbol_utils.collect_method_names { archetype_accessors }
    compiler.passes.osp_analysis --> compiler.backends.es.esast_gen_pass { OspAnalysis, OspModel, OspSlot }
    compiler.passes.osp_analysis --> compiler.backends.es.esast_gen_pass.EsastGenPass._osp_model { get_osp_model }
    type compiler.passes.osp_analysis --> compiler.backends.native.na_ir_gen_pass { OspSlot }
    compiler.passes.osp_analysis --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._compute_osp_model { get_osp_model }
    compiler.passes.osp_analysis --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._trigger_struct_names { OspAnalysis }
    type compiler.passes.osp_analysis --> compiler.frontend.codeinfo { OspModel }
    compiler.passes.ownership_hints --> cli.commands.analysis.explain { inferred_hints }
    compiler.passes.ownership_hints --> lsp.server.engine.JacLangServer.get_inlay_hints { inferred_hints }
    compiler.passes.pyast_load_pass --> cli.commands.transform.py2jac { PyastBuildPass }
    compiler.passes.pyast_load_pass --> compiler.tools.lang_tools { PyastBuildPass }
    compiler.passes.pyast_load_pass --> compiler.tools.lang_tools.AstTool.py_uni_nodes { PyastBuildPass }
    compiler.passes.rc_facts_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_expr { Ownership, result_ownership }
    compiler.passes.rc_facts_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_for_indexed { loop_body_locals }
    compiler.passes.rc_facts_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_forever { loop_body_locals }
    compiler.passes.rc_facts_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_iter_for { loop_body_locals }
    compiler.passes.rc_facts_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_open_stmt { loop_body_locals }
    compiler.passes.rc_facts_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_while { loop_body_locals }
    compiler.passes.rc_facts_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._opt_result_owned { Ownership, result_ownership }
    compiler.passes.rc_facts_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._try_chunked_for { loop_body_locals }
    compiler.passes.rc_facts_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._try_flow_for_parallel { loop_body_locals }
    compiler.passes.rc_facts_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._try_iter_protocol_for { loop_body_locals }
    compiler.passes.rc_facts_pass --> compiler.passes.ownership_check_pass.OwnershipCheckPass._nogc_infer_state { Ownership, result_ownership }
    compiler.passes.rc_facts_pass --> compiler.passes.ownership_check_pass.OwnershipCheckPass._nogc_local_shape_expr_heap { Ownership, result_ownership }
    compiler.passes.scope_walk --> compiler.passes.static_analysis_pass { ScopeWalker }
    compiler.passes.scope_walk --> compiler.tools.code_intel { ScopeWalker }
    compiler.passes.semantic_analysis_pass --> compiler.driver.pipeline { SemanticAnalysisPass }
    compiler.passes.sym_tab_build_pass --> compiler.driver.pipeline { SymTabBuildPass }
    compiler.passes.sym_tab_build_pass --> compiler.driver.program.JacProgram.load_dependency_module { SymTabBuildPass }
    compiler.passes.type_checker_pass --> compiler.passes.comptime_resolve_pass { TypeCheckPass }
    compiler.passes.type_checker_pass --> compiler.tests.test_pipeline_products { TypeCheckPass }
    compiler.passes.type_checker_pass --> compiler.tests.xbackend_equiv.compile_fixture_to_js { TypeCheckPass }
    compiler.passes.wasm_contract --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._register_na_client_import { function_contract }
    compiler.passes.wasm_contract --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass.enter_func_call { check_host_call }
    compiler.passes.annex_weave --> cli.commands.architecture | compiler.passes.import_wiring_pass | compiler.tools.jac_auto_lint_pass { import_form }
    compiler.passes.annex_weave --> compiler.driver.wiring { WovenAnnex, import_form, import_items, import_keys, relative_twin }
    compiler.passes.annex_weave --> compiler.frontend.parser.frontend { WovenAnnex, merge_annex_into, prune_generated_imports }
    compiler.passes.annex_weave --> compiler.jc_unit { merge_annex_into, prune_generated_imports }
    type compiler.passes.annex_weave --> compiler.frontend.host | compiler.frontend.kernel_host | compiler.native_compiler | project.compiler_host { WovenAnnex }
    compiler.passes.cfg_build_pass --> compiler.tools.cfg_dot { is_structural_child, unwrap_to_bool }
    compiler.passes.context --> compiler.passes.ast_validation_pass | compiler.passes.boundary_analysis_pass | compiler.passes.cfg_build_pass | compiler.passes.endpoint_effect_pass | compiler.passes.graph_lowering_pass | compiler.passes.jsx_intrinsic_guard_pass | compiler.passes.semantic_analysis_pass | compiler.passes.sym_tab_build_pass | compiler.passes.type_checker_pass | compiler.tools.doc_ir_gen_pass | compiler.tools.grammar_extract_pass | compiler.tools.jac_auto_lint_pass | compiler.tools.normalize_pass | compiler.tools.unparse_pass { TreePass }
    compiler.passes.context --> compiler.backends.native.na_compile_pass | compiler.backends.native.na_ir_gen_pass | compiler.backends.py.jcir_bc_gen_pass | compiler.driver.context_passes | compiler.driver.pass_driver | compiler.passes.access_check_pass | compiler.passes.capability_check_pass | compiler.passes.decl_impl_match_pass | compiler.passes.execution | compiler.passes.freeze_structure_pass | compiler.passes.import_wiring_pass | compiler.passes.layout_pass | compiler.passes.mtir_gen_pass | compiler.passes.ownership_check_pass | compiler.passes.pyast_load_pass | compiler.passes.rc_facts_pass | compiler.passes.region_infer_pass | compiler.passes.sem_def_match_pass | compiler.passes.static_analysis_pass | compiler.passes.variant_agreement_pass | compiler.placement.placement_solver | compiler.tools.comment_attach_pass | compiler.tools.jac_formatter_pass | project.kernel_check.pass_type_named { CompilerPass }
    compiler.passes.context --> compiler.driver.pipeline { PassSchedule }
    compiler.passes.context --> compiler.frontend.kernel_analyze | project.kernel_check { Alert }
    compiler.passes.context --> compiler.tools.cfg_dot { CompileContext, TreePass }
    type compiler.passes.context --> compiler.symbol_utils { CompilerPass }
    compiler.passes.dataflow --> compiler.passes.ownership_check_pass { DataflowTransfer, SymId }
    compiler.passes.dataflow --> compiler.passes.rc_facts_pass { SymId }
    compiler.passes.execution --> compiler.passes.pyast_load_pass.build_python_module { new_context, walk_pass }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._class_expr_bound { class_type_native_name }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._exception_handler_targets { class_type_native_name }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_archetype { EXC_MESSAGE_FIELD }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_instantiation { EXC_MESSAGE_FIELD }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._exc_message_slot { EXC_MESSAGE_FIELD }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._exc_stored_message { EXC_MESSAGE_FIELD }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._store_exc_message { EXC_MESSAGE_FIELD }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._copy_candidates { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._emit_exception_match { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._emit_subclass_str { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._get_exc_descendants { get_layout_registry }
    type compiler.passes.layout_pass --> compiler.frontend.codeinfo { LayoutRegistry }
    compiler.passes.wasm_contract --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._register_na_client_import { host_contract_dicts }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._exception_member_name { class_type_native_name }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._is_graph_type { class_type_native_name }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._register_exc_lineage { class_type_native_name }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._vtable_slot_certain { class_type_native_name }
    compiler.passes.osp_analysis --> compiler.backends.native.na_ir_gen_pass { OSP_ANY_TAGS }
    compiler.passes.context --> compiler.passes.package_boundary_pass { CompilerPass }
    compiler.passes.package_boundary_pass --> compiler.driver.pipeline { PackageBoundaryPass }
    compiler.passes.context --> compiler.backends.es.esast_gen_pass { TreePass }
    compiler.passes.context --> compiler.backends.py.jcir_gen_pass { TreePass }
    compiler.passes.context --> compiler.driver.module_compile.report_missing_native_ir { Alert }
    compiler.passes.context --> compiler.driver.progstate { CompileContext }
    compiler.passes.context --> project.kernel_check.loaded_pass_type { CompilerPass }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._erased_want { class_type_native_name }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._match_arch_name { class_type_native_name }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._module_class_name { class_type_native_name }
    compiler.passes.access_check_pass --> compiler.driver.pipeline.analysis_passes { AccessCheckPass }
    compiler.passes.capability_check_pass --> compiler.driver.pipeline.analysis_passes { PortabilityWarnPass }
    compiler.passes.capability_check_pass --> compiler.passes.placement_pass.build_native_legality { native_capability_demotion_owner, native_capability_violations }
    compiler.passes.cfg_build_pass --> compiler.driver.pipeline.flow_passes { CFGBuildPass }
    compiler.passes.cfg_build_pass --> compiler.driver.pipeline.ir_passes { CFGBuildPass }
    compiler.passes.comptime_resolve_pass --> compiler.driver.pipeline.ir_passes { ComptimeResolvePass }
    compiler.passes.context --> compiler.backends.native.na_ir_gen_pass { Alert }
    compiler.passes.context --> compiler.driver.pipeline { CompilerPass }
    compiler.passes.context --> compiler.passes.placement_pass { Alert, CompilerPass }
    compiler.passes.freeze_structure_pass --> compiler.driver.pipeline.frozen_passes { FreezeStructurePass }
    compiler.passes.jsx_intrinsic_guard_pass --> compiler.driver.pipeline.ir_passes { JsxIntrinsicGuardPass }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass { VTABLE_DROP_SLOT }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_plain_trailer { class_form_enum_member, class_form_enum_scalar }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._drop_dispatches { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._emit_default_obj_repr { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._emit_jid { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._report_unreachable_overrides { get_layout_registry }
    compiler.passes.layout_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._walk_imported_module_type_names { record_interface_twins }
    compiler.passes.layout_pass --> compiler.boundary_rules.archetype_fields { referenced_archetype }
    compiler.passes.layout_pass --> compiler.driver.pipeline.layout_passes { LayoutPass }
    compiler.passes.mtir_gen_pass --> compiler.driver.pipeline.ir_passes { MTIRGenPass }
    compiler.passes.ownership_check_pass --> compiler.driver.pipeline.analysis_passes { OwnershipCheckPass }
    compiler.passes.placement_pass --> compiler.backends.native.na_compile_pass.NativeCompilePass._run_impl { settle_native_module }
    compiler.passes.placement_pass --> compiler.backends.native.na_ir_gen_pass { NativeLegality, NativeRefusal, NativeRefused }
    compiler.passes.placement_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._demote_method_if_unlowerable { refusal_from_alert }
    compiler.passes.placement_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._lower_module { build_native_legality }
    compiler.passes.placement_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._owner_required { element_requirements }
    compiler.passes.placement_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._settle_module { settle_native_module }
    compiler.passes.placement_pass --> compiler.driver.pipeline.analysis_passes { PlacementPass }
    compiler.passes.pyast_load_pass --> compiler.driver.pipeline.python_ast_passes { PyastBuildPass }
    compiler.passes.rc_facts_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_expr { call_borrows_receiver }
    compiler.passes.rc_facts_pass --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_with_recursive { method_returns_borrow }
    compiler.passes.rc_facts_pass --> compiler.driver.pipeline.codegen_passes { RcFactsPass }
    compiler.passes.rc_facts_pass --> compiler.driver.pipeline.native_ir_passes { RcFactsPass }
    compiler.passes.rc_facts_pass --> compiler.driver.pipeline.native_lower_passes { RcFactsPass }
    compiler.passes.rc_facts_pass --> compiler.passes.ownership_check_pass.OwnershipCheckPass._nogc_infer_state { call_borrows_receiver }
    compiler.passes.region_infer_pass --> compiler.driver.pipeline.analysis_passes { RegionInferPass }
    compiler.passes.sem_def_match_pass --> compiler.driver.pipeline.ir_passes { SemDefMatchPass }
    compiler.passes.static_analysis_pass --> compiler.driver.pipeline.analysis_passes { StaticAnalysisPass }
    compiler.passes.sym_tab_build_pass --> compiler.jc_unit { SymTabBuildPass }
    compiler.passes.type_checker_pass --> compiler.driver.pipeline.analysis_passes { TypeCheckPass }
    compiler.passes.variant_agreement_pass --> compiler.driver.pipeline.analysis_passes { VariantAgreementPass }
    compiler.placement.placement --> cli.commands.fix._verify_claims { element_display_name }
    compiler.placement.placement --> compiler.driver.compiler.JacCompiler._restore_sections { summary_store }
    compiler.placement.placement --> compiler.driver.ifacecache.IfaceRegistry._persist_in_context { get_module_summary }
    compiler.placement.placement --> compiler.driver.ifacecache.IfaceRegistry._restore_placement { summary_store }
    compiler.placement.placement --> compiler.placement.placement_solver { PLACEMENT_HOLD_EXEMPT_ROOTS, get_module_summary, record_placement_evidence, scan_native_blockers, summarize_module }
    compiler.placement.placement --> compiler.placement.placement_solver._closure_pullable { module_has_root_access }
    compiler.placement.placement --> compiler.placement.placement_solver._endpoint_veto_applies { project_has_server }
    compiler.placement.placement --> compiler.placement.placement_solver._pullable_by_client_reference { module_has_root_access }
    compiler.placement.placement --> compiler.symbol_utils.client_bridged_endpoint { project_has_server }
    compiler.placement.placement --> compiler.symbol_utils.report_placement_warnings { get_module_summary }
    compiler.placement.placement --> compiler.symbol_utils.report_serverless_kind_errors { project_kind_name }
    compiler.placement.placement --> compiler.symbol_utils.serverless_server_evidence { get_module_summary, project_has_server }
    compiler.placement.placement_facts --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._dep_is_native_unit { native_unit }
    compiler.placement.placement_facts --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._register_imported_struct_types { native_unit as _typed_native_unit }
    compiler.placement.placement_facts --> compiler.driver.nativecache.NativeUnitRegistry.known_native_deps { native_unit }
    compiler.placement.placement_facts --> dist.precompile_bytecode._application_sources { module_spaces, spaces_are_client_only }
    compiler.placement.placement_facts --> dist.precompile_bytecode.find_jac_files { native_only }
    compiler.placement.placement_facts --> dist.precompile_bytecode.package_native_units { native_units_of }
    compiler.placement.placement_facts --> dist.precompile_bytecode.run_precompile { native_only }
    compiler.placement.placement_facts --> dist.precompile_bytecode.sealable_sources { discover_spaces, spaces_are_client_only }
    compiler.placement.placement_pins --> compiler.driver.boundary_classify { BareImportVerdict, classify_bare_import }
    compiler.placement.placement_pins --> compiler.driver.boundary_classify.import_declares_native_target { effective_module_pin }
    compiler.placement.placement_pins --> compiler.driver.boundary_classify.native_only_import_target { effective_module_pin }
    compiler.placement.placement_pins --> compiler.driver.boundary_classify.plain_native_import_target { effective_module_pin }
    compiler.placement.placement_pins --> compiler.passes.static_analysis_pass.StaticAnalysisPass._check_client_imports { in_client_npm_world }
    compiler.placement.placement_pins --> compiler.placement.placement.module_anchor_reasons { config_module_pin }
    compiler.placement.placement_pins --> compiler.placement.placement.project_kind_name { config_project_kind }
    compiler.placement.placement_pins --> compiler.placement.placement.summarize_module { effective_pin_for }
    compiler.placement.placement_pins --> compiler.placement.placement_facts.native_unit { effective_module_pin }
    compiler.placement.placement_pins --> compiler.placement.placement_facts.pinned_module_space { config_module_pin }
    compiler.placement.placement_pins --> compiler.placement.placement_solver._module_externally_pinned { config_module_pin }
    compiler.placement.placement_pins --> lsp.server.engine.JacLangServer._module_spec_target { in_client_npm_world }
    compiler.placement.placement_pins --> lsp.server.engine.JacLangServer._npm_item_location { in_client_npm_world }
    compiler.placement.placement_pins --> scale.tests.microservices.test_app_precompile { config_module_pin }
    compiler.placement.placement_solver --> compiler.driver.boundary_classify.plain_native_import_target { _materialize_module }
    compiler.placement.placement_solver --> compiler.driver.pipeline { PlacementApplyPass }
    compiler.placement.placement_solver --> compiler.frontend.codeinfo._inferred_native_path { native_default_path_ok }
    compiler.placement.placement_solver --> compiler.placement.placement_facts.declared_path_spaces { _materialize_module }
    compiler.placement.placement_solver --> compiler.placement.placement_facts.native_unit { native_default_path_ok }
    compiler.placement.placement_solver --> compiler.placement.placement_work.PlacementWork.drain { _pull_boundary_import }
    compiler.placement.placement_solver --> compiler.placement.placement_work.PlacementWork.refs { _ref_top_ids }
    compiler.placement.placement_solver --> dist.seal.bake_native_payloads { native_default_path_ok }
    compiler.placement.placement_work --> compiler.placement.placement_solver { PlacementWork }
    compiler.placement.placement --> compiler.placement.placement_export { ElementSummary, PLACEMENT_SCHEMA, PlacementSummary, element_display_name, get_module_summary, placement_evidence_for }
    type compiler.placement.placement --> compiler.driver.progstate { PlacementSummary }
    compiler.placement.placement_export --> cli.commands.analysis._check_file_job { collect_placement_rows }
    compiler.placement.placement_export --> cli.commands.analysis.explain { collect_placement_rows }
    compiler.placement.placement_export --> compiler.driver.ifacecache.IfaceRegistry._persist_in_context { summary_to_bytes }
    compiler.placement.placement_export --> compiler.driver.compiler.JacCompiler._restore_sections | compiler.driver.ifacecache.IfaceRegistry._restore_placement { summary_from_bytes }
    compiler.placement.placement_export --> dist.precompile_bytecode._unit_extra { summary_from_bytes, summary_to_bytes }
    compiler.placement.placement_facts --> compiler.driver.program.JacProgram.declared_codespace { native_only, native_unit }
    compiler.placement.placement_facts --> compiler.native_scope.package_host_edge { native_lowered, native_unit }
    compiler.placement.placement_facts --> dist.publish.runtime_vendor._runtime_module_options { SPACE_SERVER }
    compiler.placement.placement_facts --> project.compiler_host.ProjectHost.native_session_declares { session_declares_native }
    compiler.placement.placement_pins --> compiler.driver.program.JacProgram.declared_codespace { config_kind_space, effective_module_pin }
    compiler.placement.placement_pins --> compiler.driver.program.JacProgram.stamp_boundary_facts { config_module_pin }
    compiler.placement.placement_pins --> compiler.placement.placement_facts.session_declares_native { config_kind_space, effective_pin_for }
    type compiler.placement.placement_work --> compiler.driver.progstate { PlacementWork }
    compiler.placement.placement --> compiler.driver.nativecache._module_files_and_imports { jac_import_targets }
    compiler.placement.placement_pins --> compiler.driver.program.JacProgram.stamp_app_facts { module_dot_path }
    compiler.placement.placement --> compiler.driver.unit_products.placement_record { get_module_summary }
    compiler.placement.placement_export --> compiler.driver.unit_products.placement_record { summary_to_dict }
    compiler.placement.placement --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._owner_element { element_display_name }
    compiler.placement.placement --> compiler.driver.compiler.JacCompiler.kernel_native_entry { summary_store }
    compiler.placement.placement --> compiler.driver.compiler.JacCompiler.native_entry_engine { summary_store }
    compiler.placement.placement --> compiler.driver.module_analysis.run_analysis { record_decided }
    compiler.placement.placement --> compiler.passes.placement_pass.PlacementPass._run_undecided { record_decided }
    compiler.placement.placement --> compiler.passes.placement_pass.build_native_legality { native_blocker_scan }
    compiler.placement.placement --> compiler.passes.placement_pass.element_requirements { element_display_name }
    compiler.placement.placement --> compiler.passes.placement_pass.settle_native_module { record_decided }
    compiler.placement.placement --> compiler.placement.placement_solver { PlacementSummary, summary_store }
    compiler.placement.placement --> compiler.placement.placement_solver.PlacementApplyPass._run_impl { native_blocker_scan }
    compiler.placement.placement_facts --> compiler.driver.module_analysis.run_analysis { settle_server }
    compiler.placement.placement_facts --> compiler.driver.module_compile.admits_native_checks { variant_selected }
    compiler.placement.placement_facts --> compiler.driver.program.JacProgram.declared_codespace { variant_selected }
    compiler.placement.placement_facts --> compiler.driver.program.JacProgram.prefers_native_codespace { native_only, native_placement_hard }
    compiler.placement.placement_facts --> compiler.passes.placement_pass { native_placement_soft }
    compiler.placement.placement_facts --> compiler.passes.placement_pass.PlacementPass._run_undecided { contexts_of }
    compiler.placement.placement_facts --> compiler.passes.placement_pass.settle_native_module { settle_server }
    compiler.placement.placement_facts --> compiler.placement.placement_solver.native_closure_blocker { pinned_module_space }
    compiler.placement.placement_pins --> compiler.driver.jir._project_env_fingerprint_uncached { config_kind_space, pins_digest }
    compiler.placement.placement_pins --> compiler.driver.program.JacProgram.prefers_native_codespace { config_kind_space, effective_module_pin }
    compiler.placement.placement_pins --> compiler.passes.placement_pass.element_requirements { config_element_pin, config_pin_for }
    compiler.placement.placement_pins --> compiler.placement.placement.native_blocker_scan { config_module_pin as _cmp, config_pin_for }
    compiler.placement.placement_pins --> compiler.placement.placement.summarize_module { config_element_pin, config_module_pin }
    compiler.placement.placement_solver --> compiler.driver.module_analysis.run_analysis { placement_work }
    compiler.placement.placement_solver --> compiler.driver.pipeline.place_module { refresh_placement_module, solve_program_placement }
    compiler.placement.placement_solver --> compiler.driver.program.JacProgram.parse_source { native_placement_candidate }
    compiler.placement.placement_solver --> compiler.passes.placement_pass.PlacementPass._run_decided { placement_work, refresh_placement_module, solve_module_placement }
    compiler.placement.placement_solver --> compiler.passes.placement_pass.PlacementPass._run_undecided { native_placement_candidate, placement_work, refresh_placement_module, solve_module_placement }
    compiler.placement.placement_solver --> compiler.passes.placement_pass.build_native_legality { native_closure_blocker }
    compiler.placement.placement_solver --> compiler.passes.placement_pass.settle_native_module { invalidate_importers_es }
    compiler.placement.placement_solver --> compiler.passes.placement_pass.uncrossable_native { placement_work, refresh_placement_module }
    compiler.placement.placement --> compiler.frontend.kernel_host.KernelHost.python_module { summary_store }
    compiler.placement.placement_export --> compiler.frontend.kernel_host.KernelHost.python_module { summary_from_dict }
    compiler.tests.xbackend_equiv --> compiler.tests.test_fixed_width_equivalence { call_py_fixture, compile_fixture_to_js, encode_py_wire, run_js_expr, run_js_function, run_py_fixture, run_with_both }
    compiler.tests.xbackend_equiv --> compiler.tests.test_graph_fragment_equivalence { run_js_module_fixture, run_py_fixture, run_with_both }
    compiler.tests.xbackend_equiv --> compiler.tests.test_native_list_search_equality { compile_native, get_func }
    compiler.tests.xbackend_equiv --> compiler.tests.test_osp_equivalence { compile_native, run_native_function, run_py_fixture, run_with_both }
    compiler.tests.xbackend_equiv --> compiler.tests.test_prim_equivalence { compare_results, compile_fixture_to_js, compile_native, compile_native_errors, get_func, run_js_function, run_py_fixture, run_with_both }
    compiler.tests.xbackend_equiv --> compiler.tests.test_shared_types_equivalence { run_with_both }
    compiler.tests.xbackend_equiv --> compiler.tests.test_socket_equivalence { compile_native, get_func, run_py_fixture }
    compiler.tests.xbackend_equiv --> compiler.tests.test_ssl_equivalence { compile_native, get_func, run_py_fixture }
    compiler.tests.xbackend_equiv --> compiler.tests.test_tarfile_equivalence { FIXTURES, get_func, remember_engine_unit, run_py_fixture }
    compiler.tests.xbackend_equiv --> compiler.tests.test_urllib_equivalence { compile_native, get_func, run_py_fixture }
    compiler.tests.xbackend_equiv --> compiler.tests.test_xbackend_equiv { run_js_expr, run_js_function }
    compiler.tests.xbackend_equiv --> compiler.tests.test_zstd_equivalence { FIXTURES, compare_results, remember_engine_unit, run_native_function, run_py_fixture }
    compiler.tests.xbackend_equiv --> compiler.tests.test_loop_closure_equivalence { compile_fixture_to_js, run_js_function, run_py_fixture, run_with_both }
    compiler.tools.code_intel --> cli.commands.code { CodeIntelligence }
    compiler.tools.code_intel --> compiler.tests.test_code_intel { CodeIntelligence }
    type compiler.tools.doc_ir --> compiler.frontend.codeinfo { Doc }
    compiler.tools.doc_ir as doc --> compiler.frontend.codeinfo.CodeGenTarget.doc_ir.getter;
    compiler.tools.doc_ir as doc --> compiler.tools.doc_ir_gen_pass;
    compiler.tools.doc_ir as doc --> compiler.tools.jac_formatter_pass;
    compiler.tools.doc_ir_gen_pass --> compiler.tools.jac_formatter_pass.format_module { DocIRGenPass }
    compiler.tools.doc_ir_gen_pass --> compiler.tools.lang_tools { DocIRGenPass }
    compiler.tools.grammar_extract_pass --> cli.commands.analysis.grammar { GrammarExtractPass }
    compiler.tools.lang_tools --> cli.commands.tools.tool { AstTool }
    compiler.tools.reactive_use_walk --> compiler.tools.jac_auto_lint_pass { ReactiveUseWalker }
    compiler.tools.treeprinter --> cli.mcp.compiler_bridge { node_to_dict, print_ast_tree }
    compiler.tools.treeprinter --> compiler.tools.lang_tools { print_ast_tree, print_symtab_tree, printgraph_ast_tree, printgraph_symtab_tree }
    compiler.tools.cfg_dot --> compiler.tools.lang_tools { cfg_dot_from_file }
    compiler.tools.jac_formatter_pass --> cli.commands.transform.py2jac | cli.mcp.compiler_bridge | compiler.tools.lang_tools { unparse_module }
    compiler.tools.normalize_pass --> compiler.tools.jac_formatter_pass.unparse_module { NormalizePass }
    compiler.tools.cfg_dot --> compiler.driver.pipeline.cfg_dot_passes { CoalesceBBPass }
    compiler.tools.comment_attach_pass --> compiler.driver.pipeline.format_lintfix_passes { CommentAttachPass }
    compiler.tools.comment_attach_pass --> compiler.driver.pipeline.format_passes { CommentAttachPass }
    compiler.tools.doc_ir_gen_pass --> compiler.driver.pipeline.doc_passes { DocIRGenPass }
    compiler.tools.doc_ir_gen_pass --> compiler.driver.pipeline.format_lintfix_passes { DocIRGenPass }
    compiler.tools.doc_ir_gen_pass --> compiler.driver.pipeline.format_passes { DocIRGenPass }
    compiler.tools.grammar_extract_pass --> compiler.driver.pipeline.grammar_passes { GrammarExtractPass }
    compiler.tools.jac_auto_lint_pass --> compiler.driver.pipeline.analysis_passes { JacLintCheckPass }
    compiler.tools.jac_auto_lint_pass --> compiler.driver.pipeline.format_lintfix_passes { JacAutoLintPass }
    compiler.tools.jac_auto_lint_pass --> compiler.driver.pipeline.lint_passes { JacLintCheckPass }
    compiler.tools.jac_formatter_pass --> compiler.driver.pipeline.format_lintfix_passes { JacFormatPass }
    compiler.tools.jac_formatter_pass --> compiler.driver.pipeline.format_passes { JacFormatPass }
    compiler.tools.jac_formatter_pass --> compiler.driver.pipeline.format_text_passes { JacFormatPass }
    compiler.tools.normalize_pass --> compiler.driver.pipeline.normalize_passes { NormalizePass }
    compiler.tools.unparse_pass --> compiler.driver.pipeline.unparse_passes { UnparsePass }
    compiler.types.builtin_extensions --> compiler.types.type_evaluator { install_builtin_extensions }
    compiler.types.ct_eval --> compiler.types.type_evaluator { CtEvaluator }
    compiler.types.ct_value --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._instantiate_generic { ct_mangle }
    type compiler.types.ct_value --> compiler.frontend.unitree { CtValue }
    compiler.types.ct_value --> compiler.passes.type_checker_pass { CT_DEFERRED, CtValue }
    compiler.types.ct_value --> compiler.types.ct_eval { CT_DEFERRED, CtDeferred, CtEnumMember, CtFunc, CtRecord, CtType, CtValue }
    compiler.types.ct_value --> compiler.types.type_evaluator { CtValue }
    compiler.types.enum_utils --> compiler.types.type_evaluator { build_enum_members, get_special_enum_value_type_from_bases }
    compiler.types.fixed_width --> compiler.passes.type_checker_pass.TypeCheckPass._provably_in_range { interval_of_expr, interval_of_op }
    compiler.types.fixed_width --> compiler.passes.type_checker_pass.TypeCheckPass._stamp_fixed_width { numeric_name_of }
    compiler.types.fixed_width --> compiler.types.operations { arithmetic_result_type, both_numeric, folded_number, numeric_name_of, shift_result_type, unify_numeric_operands }
    compiler.types.fixed_width --> compiler.types.type_evaluator { AssignVerdict, arithmetic_result_type, assign_numeric_expr, both_numeric, fixed_width_call_type, is_unsigned_type, unify_numeric_operands }
    compiler.types.fixed_width --> compiler.types.type_evaluator.TypeEvaluator._extern_field_type { numeric_name_of }
    compiler.types.fixed_width --> compiler.types.type_evaluator.TypeEvaluator._get_type_from_flow_node { numeric_name_of }
    compiler.types.operations --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._emit_arch_dunder_binop { BINARY_OPERATOR_MAP }
    compiler.types.operations --> compiler.passes.type_checker_pass { ARITHMETIC_OPERATORS, AUG_OPERATOR_MAP, AUG_TO_BINARY_MAP, BINARY_OPERATOR_MAP, BITWISE_OPERATORS, COMPLEX_ARITH_OPS, SHIFT_OPERATORS, get_complex_arith_result_type, get_numeric_promotion_type, get_pow_result_type }
    compiler.types.operations --> compiler.types.type_evaluator { BINARY_OPERATOR_MAP, get_type_of_binary_operation, is_annotation_type }
    compiler.types.ownership --> compiler.passes.ownership_check_pass.OwnershipCheckPass._view_arch_of_call { contains_borrow }
    compiler.types.properties --> compiler.types.type_evaluator { is_cached_property_decorator_type, is_property_decorator_type }
    compiler.types.ts_decl_parser --> compiler.tests.test_jac_mobui_typing { parse_dts }
    compiler.types.ts_decl_parser --> compiler.types.type_evaluator { TsAccess, TsDecl, TsDeclKind, TsMember, TsType, TsTypeKind, ts_decl_binding_kind }
    compiler.types.ts_decl_parser --> compiler.types.type_evaluator.TypeEvaluator._load_ts_declarations { parse_dts }
    type compiler.types.type_evaluator --> compiler.driver.program { TypeEvaluator }
    compiler.types.type_evaluator --> compiler.driver.program.JacProgram.get_type_evaluator { TypeEvaluator }
    type compiler.types.type_evaluator --> compiler.passes.type_checker_pass { TypeEvaluator }
    compiler.types.type_evaluator --> compiler.tests.test_jac_mobui_typing { FunctionType, UnknownType }
    type compiler.types.type_evaluator --> compiler.types.ct_eval { TypeEvaluator }
    type compiler.types.type_evaluator --> compiler.types.enum_utils { PrefetchedTypes, TypeEvaluator }
    type compiler.types.type_evaluator --> compiler.types.fixed_width { TypeEvaluator }
    type compiler.types.type_evaluator --> compiler.types.operations { TypeEvaluator }
    type compiler.types.type_evaluator --> compiler.types.type_utils { TypeEvaluator }
    compiler.types.type_evaluator --> dist.precompile_bytecode.precompile_unit_context;
    compiler.types.type_utils --> compiler.backends.es.esast_gen_pass.EsastGenPass._expr_type_name { expr_primitive_name }
    compiler.types.type_utils --> compiler.backends.es.esast_gen_pass.EsastGenPass._resolve_primitive_type_name { primitive_type_name_of }
    compiler.types.type_utils --> compiler.backends.es.esast_gen_pass.EsastGenPass._try_primitive_op { expr_primitive_name }
    compiler.types.type_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._agg_key_args { primitive_type_name_of }
    compiler.types.type_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._container_class_name { primitive_type_name_of }
    compiler.types.type_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._is_boolean_result_expr { primitive_type_name_of }
    compiler.types.type_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._key_elem_unsigned { primitive_type_name_of }
    compiler.types.type_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._lower_coercion { primitive_type_name_of }
    compiler.types.type_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._match_subj_ty { convert_to_instance }
    compiler.types.type_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._scalar_shape { primitive_type_name_of }
    compiler.types.type_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._sort_key_orderable { primitive_type_name_of }
    compiler.types.type_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._sort_key_unsigned { primitive_type_name_of }
    compiler.types.type_utils --> compiler.passes.static_analysis_pass.StaticAnalysisPass._check_semantic_patterns { expr_primitive_name }
    compiler.types.type_utils --> compiler.passes.type_checker_pass { BARE_GENERIC_REQUIRED, PropertyWriteKind, get_declared_generator_return_type, get_generator_yield_type, is_generator_family_type }
    compiler.types.type_utils --> compiler.tests.test_property_write_kind { PropertyWriteKind }
    compiler.types.type_utils --> compiler.types.ct_eval { lookup_symtab }
    compiler.types.type_utils --> compiler.types.ownership { apply_solved_type_vars, build_type_var_solution }
    compiler.types.type_utils --> compiler.types.stubcat.writer.CatalogWriter.property_facts { PropertyWriteKind }
    compiler.types.type_utils --> compiler.types.type_evaluator { ClassMember, ParamAssignmentTracker, PropertyWriteKind, PropertyWriteResult, apply_solved_type_vars, build_type_var_solution, class_implements_protocol, collect_member_syms, compute_module_source_flags, compute_mro_linearization, convert_to_instance, get_declared_generator_return_type, is_generator_family_type, lookup_symtab, shadowed_type_var_names, specialize_for_base_class, synthesize_self_type_var }
    compiler.types.type_utils --> compiler.types.type_evaluator.TypeEvaluator._apply_function_decorators { apply_solved_type_vars }
    compiler.types.type_utils --> compiler.types.type_evaluator.TypeEvaluator._classify_property_symbol { PropertyWriteKind }
    compiler.types.type_utils --> compiler.types.type_evaluator.TypeEvaluator._get_getattr_return_type { collect_member_syms }
    compiler.types.type_utils --> compiler.types.type_evaluator.TypeEvaluator._get_type_of_expression_core { PropertyWriteKind, synthesize_self_type_var }
    compiler.types.type_utils --> compiler.types.type_evaluator.TypeEvaluator._heal_ancestry { ensure_mro_fresh }
    compiler.types.type_utils --> compiler.types.type_evaluator.TypeEvaluator._heal_class_bases { linearize_mro, mro_signature }
    compiler.types.type_utils --> compiler.types.type_evaluator.TypeEvaluator._lookup_class_member { ensure_mro_fresh }
    compiler.types.type_utils --> compiler.types.type_evaluator.TypeEvaluator._super_owner_for { collect_member_syms }
    compiler.types.type_utils --> compiler.types.type_evaluator.TypeEvaluator._type_in_list { types_equivalent }
    compiler.types.type_utils --> compiler.types.type_evaluator.TypeEvaluator.get_getter_type_from_property { PropertyWriteKind }
    compiler.types.type_utils --> compiler.types.type_evaluator.TypeEvaluator.get_property_write_type { PropertyWriteKind, PropertyWriteResult }
    compiler.types.type_utils --> compiler.types.type_evaluator.TypeEvaluator.is_sub_class { ensure_mro_fresh }
    compiler.types.type_utils --> compiler.types.types.ClassType.lookup_member_symbol { collect_member_syms, ensure_mro_fresh }
    compiler.types.type_utils --> compiler.types.types.FunctionType.specialize { apply_solved_type_vars, build_type_var_solution }
    compiler.types.type_utils --> compiler.types.types.FunctionType.specialize_func_type_vars { apply_solved_type_vars }
    compiler.types.type_utils --> lsp.server.utils { compute_mro_linearization }
    compiler.types.types --> compiler.backends.es.esast_gen_pass { ClassType, TypeBase }
    compiler.types.types --> compiler.backends.es.esast_gen_pass.EsastGenPass._arch_kind_of_type { ClassType }
    compiler.types.types --> compiler.backends.es.esast_gen_pass.EsastGenPass._exit_name_impl { ClassType as _ClassType }
    compiler.types.types --> compiler.backends.es.esast_gen_pass.EsastGenPass._field_constructor_args { ClassType }
    compiler.types.types --> compiler.backends.es.esast_gen_pass.EsastGenPass._osp_expr_arch_name { ClassType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass { ClassType, FunctionType as SemanticFunctionType, ModuleType, Parameter, TypeBase, UnionType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._agg_key_args { ClassType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._aos_elem_name { ClassType as _AeClassType, TypeVarType as _AeTypeVarType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._apply_flow_narrowing { ClassType as _ClassType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._c_scalar_llvm { ClassType as _CClassType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_archetype { FunctionType as _ClibFnType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._container_class_name { ClassType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._elem_arch_name_of { ClassType as _ClassType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._elem_storage_llvm { ClassType as _EsClassType, UnionType as _EsUnionType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._enum_name_of { ClassType as EnumClassType, EnumMemberType, TypeBase, UnionType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._enum_union_tags { ClassType as _EnClassType, EnumMemberType as _EnMemberType, UnionType as _EnUnionType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._erased_seq_type { ClassType as _EsqClassType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._erased_typevar_names { TypeVarType as _EtvTypeVarType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._foreign_optional_field { ClassType as _FofClassType, TypeVarType as _FofTypeVarType, UnionType as _FofUnionType, UnknownType as _FofUnknownType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._instantiate_generic_for_target { FunctionType as _A5FnType, TypeVarType as _A5TypeVar }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._is_runtime_class_tuple { ClassType as _SeqClassType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._isinstance_abc_reduction { ClassType as _AbcClassType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._lower_type { AnyType as _AnyType, ClassType as _ClassType, EnumMemberType as _EnumMemberType, FunctionType as _FunctionType, NeverType as _NeverType, TypeVarType as _TypeVarType, UnionType as _UnionType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._lower_view_container { ClassType as _VcClassType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._opt_sole_member { ClassType as _OsClassType, UnionType as _OsUnionType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._osp_disc_list_operand { ClassType as _DiscClassType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._resolve_field_type { TypeVarType as _RfTypeVarType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._solve_generic_call { ClassType as _CT, TypeVarType as _TVT, UnionType as _UT }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._sort_key_orderable { ClassType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._sort_key_return_type { FunctionType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._spec_union_agreement { ClassType as _SuClassType, UnionType as _SuUnionType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._syntactic_bind_type_params { ClassType as _SbCT }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._type_base_is_unknown { UnknownType as _UnknownType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._typevar_optional_field { ClassType as _TvoClassType, TypeVarType as _TvoTypeVarType, UnionType as _TvoUnionType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._unbox_narrowed_member { ClassType as _ClassType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._variadic_tuple_seq_type { UnknownType as _VtUnknown }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._widened_tuple_decl_type { ClassType as _WdClassType }
    compiler.types.types --> compiler.backends.py.jcir_gen_pass.JcirGenPass._clib_block_desc { FunctionType }
    compiler.types.types --> compiler.c_interop.c_type_arg { AnyType, ClassType, UnknownType }
    compiler.types.types --> compiler.c_interop.c_type_spec { ClassType, FunctionType, UnionType }
    type compiler.types.types --> compiler.frontend.relations { ClassDetailsPrivate, ClassDetailsShared, ClassType, EnumMemberInfo, EnumMemberType, FunctionType, ModuleType, OverloadedType, Parameter, TypeBase, TypeVarType, UnionType }
    type compiler.types.types --> compiler.frontend.unitree { TypeBase }
    compiler.types.types --> compiler.frontend.unitree.DeleteStmt.type_has_graph_member { ClassType, TypeVarType, UnionType }
    compiler.types.types --> compiler.frontend.unitree.DeleteStmt.type_may_hold_graph { ClassType, UnionType }
    compiler.types.types --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass.enter_atom_trailer { ClassType }
    type compiler.types.types --> compiler.passes.layout_pass { TypeBase }
    compiler.types.types --> compiler.passes.layout_pass.LayoutPass._is_layout_compatible_semantic_type { ClassType, FunctionType, UnionType }
    compiler.types.types --> compiler.passes.layout_pass.class_form_enum_member { EnumMemberType as _EnumMemberType }
    compiler.types.types --> compiler.passes.layout_pass.class_type_native_name { ClassType }
    compiler.types.types --> compiler.passes.layout_pass.declaring_module_path { ClassType }
    compiler.types.types --> compiler.passes.layout_pass.is_enum_class_type { ClassType as _ClassType }
    compiler.types.types --> compiler.passes.layout_pass.native_type_key { ClassType, FunctionType, OverloadedType, UnionType }
    compiler.types.types --> compiler.passes.layout_pass.referenced_archetype { ClassType }
    compiler.types.types --> compiler.passes.ownership_check_pass { FunctionType }
    compiler.types.types --> compiler.passes.ownership_check_pass.OwnershipCheckPass._emit_place_intrinsic_diagnostics { ClassType, TypeBase, UnionType }
    compiler.types.types --> compiler.passes.ownership_check_pass.OwnershipCheckPass._handled_by_enclosing_try { ClassType }
    compiler.types.types --> compiler.passes.ownership_check_pass.OwnershipCheckPass._nogc_infer_locals { AnyType }
    compiler.types.types --> compiler.passes.ownership_check_pass.OwnershipCheckPass._view_arch_of_call { ClassType }
    compiler.types.types --> compiler.passes.ownership_check_pass._is_class_object { ClassType }
    compiler.types.types --> compiler.passes.type_checker_pass { AnyType, ClassType, FunctionType, ModuleType, TypeBase, TypeVarType, UnionType, UnknownType }
    compiler.types.types --> compiler.passes.type_checker_pass.TypeCheckPass._install_client_state_setters { create_callable_type }
    compiler.types.types --> compiler.passes.wasm_contract.check_host_call { ClassType, FunctionType }
    compiler.types.types --> compiler.symbol_utils.imported_module_name { ModuleType }
    compiler.types.types --> compiler.tests.test_stubcat_roundtrip { ClassType, FunctionType, OverloadedType }
    compiler.types.types --> compiler.types.builtin_extensions { ClassType, FunctionType, FunctionTypeFlags, Parameter, ParameterCategory, TypeBase }
    compiler.types.types --> compiler.types.ct_eval { ClassType, ModuleType, TypeBase, UnknownType }
    type compiler.types.types --> compiler.types.ct_value { ClassType, TypeBase }
    compiler.types.types --> compiler.types.enum_utils { ClassType, EnumMemberInfo, TypeBase }
    compiler.types.types --> compiler.types.fixed_width { AnyType, ClassType, TypeBase, UnionType, UnknownType }
    compiler.types.types --> compiler.types.operations { AnyType, ClassType, FunctionType, NeverType, TypeBase, TypeVarType, UnionType, UnknownType }
    compiler.types.types --> compiler.types.ownership { ClassType, TypeBase, UnionType }
    compiler.types.types --> compiler.types.properties { ClassType, TypeBase }
    compiler.types.types --> compiler.types.stubcat.reader { AnyType, ClassDetailsPrivate, ClassDetailsShared, ClassType, EnumMemberInfo, EnumMemberType, FunctionType, ModuleType, NeverType, OverloadedType, Parameter, ParameterCategory, TypeBase, TypeFlags, TypeVarType, UnionType, UnknownType }
    compiler.types.types --> compiler.types.stubcat.writer { AnyType, ClassDetailsShared, ClassType, EnumMemberInfo, EnumMemberType, FunctionType, ModuleType, NeverType, OverloadedType, Parameter, TypeBase, TypeVarType, UnionType, UnknownType }
    compiler.types.types --> compiler.types.type_evaluator { AnyType, ClassDetailsPrivate, ClassDetailsShared, ClassType, EnumMemberInfo, EnumMemberType, FunctionType, FunctionTypeFlags, ModuleType, NeverType, OverloadedType, Parameter, ParameterCategory, TypeBase, TypeCategory, TypeFlags, TypeVarType, UnionType, UnknownType, create_callable_type }
    compiler.types.types --> compiler.types.type_evaluator.TypeEvaluator._extern_field_type { create_callable_type }
    compiler.types.types --> compiler.types.type_utils { AnyType, ClassType, EnumMemberType, FunctionType, NeverType, Parameter, TypeBase, TypeVarType, UnionType, UnknownType }
    compiler.types.types --> lsp.server.engine { ClassType, FunctionType, ModuleType, OverloadedType, TypeBase }
    compiler.types.types --> lsp.server.utils { ClassType, ModuleType, TypeBase }
    compiler.types.ct_builtins --> compiler.types.ct_eval { CT_BUILTIN_EXCEPTIONS, CT_BUILTIN_FUNCS, CT_BUILTIN_TYPES, ct_call_builtin, ct_call_method, ct_call_method_value, ct_construct_builtin, ct_type_attr, ct_value_attr }
    type compiler.types.ct_eval --> compiler.backends.native.na_ir_gen_pass { CtEvaluator }
    compiler.types.ct_format --> compiler.types.ct_builtins { ct_binary, ct_format, ct_str_format, pad_text }
    compiler.types.ct_format --> compiler.types.ct_eval { ct_binary, ct_convert, ct_format, ct_inplace }
    compiler.types.ct_int --> compiler.types.ct_builtins { MAX_STR_DIGITS, mag_bit_length, mag_divmod, mag_from_int, mag_gcd, mag_isqrt, mag_low_bits_nonzero, mag_mul, mag_shl, mag_shr, mag_to_int }
    compiler.types.ct_int --> compiler.types.ct_ops { MAG_MASK, MAG_SHIFT, MAX_STR_DIGITS, mag_add, mag_add_small, mag_bit_length, mag_cmp, mag_divmod, mag_from_int, mag_low_bits_nonzero, mag_mul, mag_parse_digits, mag_shl, mag_shr, mag_sub, mag_to_int, mag_to_pow2_str, twos_limbs, twos_to_signed }
    compiler.types.ct_int --> compiler.types.ct_value { MAX_STR_DIGITS, mag_add_small, mag_bit_length, mag_cmp, mag_decimal_digits, mag_from_int, mag_shl, mag_to_int }
    compiler.types.ct_ops --> compiler.types.ct_builtins { ct_binop, ct_contains, ct_hash, ct_int_parse, ct_lt, ct_order, float_divmod, float_round_to_int, int_abs, int_add, int_bit_length, int_divmod, int_is_neg, int_is_zero, int_mul, int_prefixed, int_round, int_sub, int_to_float, set_algebra, slice_indices }
    compiler.types.ct_ops --> compiler.types.ct_eval { ct_compare, ct_getitem, ct_getslice, ct_int_literal, ct_setitem, ct_symbol, ct_unary, int_add, int_cmp }
    compiler.types.ct_ops --> compiler.types.ct_format { ct_binop, ct_getitem, int_abs, int_is_neg, int_to_base_str, int_to_float, set_algebra }
    compiler.types.ct_value --> compiler.backends.es.esast_gen_pass { CtBool, CtDict, CtFloat, CtInt, CtList, CtNone, CtSet, CtStr, CtTuple, CtValue, int_host }
    compiler.types.ct_value --> compiler.backends.native.na_ir_gen_pass { CtBool, CtBytes, CtFloat, CtInt, CtNone, CtStr, CtValue, ct_iter, ct_mangle, ct_truthy }
    compiler.types.ct_value --> compiler.backends.py.jcir_gen_pass.JcirGenPass._ct_kind { CtBool, CtBytes, CtDict, CtEnumMember, CtFloat, CtFunc, CtInt, CtList, CtNone, CtRecord, CtSet, CtStr, CtTuple, CtType, ct_host_scalar, ct_is_materializable, ct_is_scalar, ct_repr }
    compiler.types.ct_value --> compiler.backends.py.jcir_gen_pass.JcirGenPass._ct_materializable { CtBool, CtBytes, CtDict, CtEnumMember, CtFloat, CtFunc, CtInt, CtList, CtNone, CtRecord, CtSet, CtStr, CtTuple, CtType, ct_host_scalar, ct_is_materializable, ct_is_scalar, ct_repr }
    compiler.types.ct_value --> compiler.backends.py.jcir_gen_pass.JcirGenPass._ct_order_key { CtBool, CtBytes, CtDict, CtEnumMember, CtFloat, CtFunc, CtInt, CtList, CtNone, CtRecord, CtSet, CtStr, CtTuple, CtType, ct_host_scalar, ct_is_materializable, ct_is_scalar, ct_repr }
    compiler.types.ct_value --> compiler.backends.py.jcir_gen_pass.JcirGenPass._materialize { CtBool, CtBytes, CtDict, CtEnumMember, CtFloat, CtFunc, CtInt, CtList, CtNone, CtRecord, CtSet, CtStr, CtTuple, CtType, ct_host_scalar, ct_is_materializable, ct_is_scalar, ct_repr }
    compiler.types.ct_value --> compiler.frontend.host.HostServices.ct_environment | compiler.frontend.kernel_inputs | project.compiler_host.ProjectHost.ct_environment { CtEnvironment }
    compiler.types.ct_value --> compiler.passes.type_checker_pass { ct_is_iterable, ct_str, ct_truthy, ct_type_name }
    compiler.types.ct_value --> compiler.types.ct_builtins { CT_FALSE, CT_NONE, CT_TRUE, CtBool, CtBuiltin, CtBytes, CtCaller, CtDict, CtError, CtExc, CtFloat, CtInt, CtList, CtMethod, CtModule, CtNone, CtRange, CtSet, CtStr, CtTuple, CtValue, CtView, as_ct_int, ct_eq, ct_exc, ct_exc_value, ct_iter, ct_len, ct_repr, ct_same_or_eq, ct_str, ct_truthy, ct_type_name, dict_copy, dict_delete, dict_get, dict_set, float_ceil, float_floor, float_to_ct_int, int_cmp, int_sign_mag, mk_bool, mk_bytes, mk_dict, mk_float, mk_int, mk_int_mag, mk_list, mk_set, mk_str, mk_tuple, range_len, set_add, set_discard, set_has }
    compiler.types.ct_value --> compiler.types.ct_eval { CT_NONE, CtBool, CtBound, CtBuiltin, CtBytes, CtCaller, CtDeferredSignal, CtDict, CtEnvironment, CtError, CtExc, CtFloat, CtInt, CtList, CtMethod, CtModule, CtNone, CtNotComptime, CtRaise, CtRange, CtSet, CtStr, CtTuple, CtView, as_ct_int, ascii_escape, ct_eq, ct_exc, ct_exc_is, ct_iter, ct_repr, ct_str, ct_truthy, ct_type_name, dict_set, mk_bool, mk_bytes, mk_dict, mk_float, mk_int, mk_list, mk_set, mk_str, mk_tuple, range_len, set_add }
    compiler.types.ct_value --> compiler.types.ct_format { CtBool, CtBytes, CtDict, CtEnumMember, CtError, CtFloat, CtInt, CtList, CtNone, CtRecord, CtSet, CtStr, CtTuple, CtValue, as_ct_int, ascii_escape, ct_exc, ct_exc_value, ct_iter, ct_repr, ct_str, ct_type_name, dict_get, dict_set, float_to_ct_int, int_decimal, mk_str }
    compiler.types.ct_value --> compiler.types.ct_ops { CT_FALSE, CT_NONE, CT_TRUE, CtBool, CtBytes, CtDeferred, CtDeferredSignal, CtDict, CtEnumMember, CtError, CtFloat, CtFunc, CtInt, CtList, CtNone, CtRaise, CtRange, CtRecord, CtSet, CtStr, CtTuple, CtType, CtValue, CtView, as_ct_int, bytes_has, ct_eq, ct_exc, ct_exc_value, ct_is_unhashable, ct_iter, ct_len, ct_repr, ct_same_or_eq, ct_str, ct_truthy, ct_type_name, dict_copy, dict_get, dict_key_of, dict_set, float_floor, float_to_ct_int, int_cmp, int_decimal, int_float_cmp, int_sign_mag, mk_bool, mk_bytes, mk_float, mk_int, mk_int_mag, mk_list, mk_set, mk_str, mk_tuple, range_len, set_add, set_has, set_key_of, view_items_set }
    type compiler.types.ct_value --> compiler.backends.py.jcir_gen_pass { CtRecord, CtValue }
    type compiler.types.ct_value --> compiler.frontend.host | compiler.frontend.kernel_host | project.compiler_host { CtEnvironment }
    type compiler.types.ct_value --> compiler.types.types { CtValue }
    compiler.types.type_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_call | compiler.passes.ownership_check_pass { is_builtin_region_type }
    compiler.types.type_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._codegen_method_call_inner { is_builtin_region_type }
    compiler.types.type_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._lower_partition_unpack { is_builtin_region_type }
    compiler.types.type_utils --> compiler.passes.rc_facts_pass.RcFactsPass._asn_makes_region_handle { expr_is_builtin_region }
    compiler.types.types --> compiler.backends.es.esast_gen_pass.EsastGenPass._build_spawn_runtime_call | compiler.backends.native.na_ir_gen_pass.NaIRGenPass._exception_handler_targets | compiler.passes.capability_check_pass | compiler.passes.layout_pass.class_form_enum_scalar | compiler.passes.ownership_check_pass.OwnershipCheckPass._raised_class_names { ClassType }
    compiler.types.types --> compiler.passes.layout_pass.enum_class_of { ClassType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._class_expr_bound { TypeVarType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._erased_decl { ClassType as _EdClassType, TypeVarType as _EdTypeVarType, UnionType as _EdUnionType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._erased_decl_names { TypeVarType as _EnTypeVarType, UnionType as _EnUnionType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._is_object_union_key | compiler.passes.ownership_check_pass { ClassType, UnionType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._typevar_bound_struct { ClassType, TypeVarType, UnionType }
    compiler.types.types --> compiler.frontend.kernel_host { ClassDetailsShared, ClassType, TypeBase }
    compiler.types.types --> compiler.passes.capability_check_pass._class_bounded_typevar { ClassType, TypeVarType }
    compiler.types.types --> compiler.passes.layout_pass.class_form_enum_member { EnumMemberType }
    type compiler.types.types --> compiler.c_interop { ClassType, TypeBase }
    type compiler.types.types --> compiler.driver.ifacecache | compiler.types.stubcat.resolver { ClassDetailsShared }
    type compiler.types.types --> compiler.passes.layout_pass { ClassType }
    type compiler.types.types --> compiler.passes.ownership_check_pass { TypeBase }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._exception_member_name { ClassType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._is_graph_type { ClassType as _GtClassType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._register_exc_lineage { ClassType, TypeBase }
    type compiler.types.types --> compiler.backends.native.primitives_native { TypeBase }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._sort_key_orderable { UnknownType }
    compiler.types.types --> packages.api { ClassType, FunctionType, ParamKind }
    compiler.types.ct_int --> compiler.types.ct_value { MAG_SHIFT }
    type compiler.types.ct_value --> compiler.backends.py.jcir_gen_pass { CtInt }
    compiler.types.ct_value --> compiler.backends.py.jcir_gen_pass.JcirGenPass.int_const_of { int_host, int_wide_bytes }
    compiler.types.operations --> compiler.backends.es.esast_gen_pass { AUG_TO_BINARY_MAP }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._typed_elem_llvm_of { TypeVarType as _TeTypeVar }
    type compiler.types.types --> compiler.passes.layout_pass { ClassDetailsShared }
    compiler.types.type_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._check_native_import_names { lookup_symtab }
    compiler.types.type_utils --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._is_number_slot { primitive_type_name_of }
    compiler.types.types --> compiler.backends.es.esast_gen_pass.EsastGenPass._builtin_param_names { FunctionType, ParameterCategory }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._emit_jid { ClassType, UnionType }
    compiler.types.types --> compiler.backends.native.na_ir_gen_pass.NaIRGenPass._lower_clib_function_type { FunctionType as CallbackType }
    compiler.types.types --> compiler.c_interop._ambient_c_call_returns { FunctionType, OverloadedType }
    compiler.types.types --> compiler.c_interop.c_param_type { FunctionType }
    compiler.types.types --> compiler.native_bindings { ClassType, FunctionType, OverloadedType, TypeBase }
    compiler.types.types --> compiler.passes.layout_pass.record_interface_twins { ClassType }
    compiler.types.types --> compiler.passes.layout_pass.referenced_native_name { ClassType }
    compiler.types.types --> compiler.types.type_utils { CLASS_GRAPH_EPOCH }
    compiler.types.stubcat.build as catalog_build --> compiler.tests.test_stubcat_roundtrip;
    compiler.types.stubcat.build --> compiler.tests.test_stubcat_roundtrip { build_catalog }
    compiler.types.stubcat.format --> compiler.driver.compiler.JacCompiler.ensure_stub_catalog;
    compiler.types.stubcat.format --> compiler.types.stubcat.locate { FORMAT_VERSION }
    compiler.types.stubcat.format --> compiler.types.stubcat.reader { ACCESS_PRIVATE, ACCESS_PROTECTED, Cursor, Header, LIT_BOOL, LIT_INT, LIT_STR, MOD_EXTERNAL, PM_CLS, PM_COMPTIME, PM_HAS_DEFAULT, PM_SELF, SC_MODULE, SH_BUILTIN, SH_DATACLASS, SH_ENUM, SH_NAMEDTUPLE, SH_ROOT, SH_STDLIB, SH_TYPEDDICT, SH_XREF, SYMF_FINAL, SYMF_NA_ESCAPES, SYMF_NA_REGION_HANDLE, SYMF_NA_STACK_OK, SYMF_PARAM_REBOUND, SYMF_READONLY, TV_CLASS_PARAM, TV_CONTRAVARIANT, TV_COVARIANT, TV_PARAM_SPEC, TV_SELF, TY_ANY, TY_CLASS, TY_ENUM_MEMBER, TY_FUNCTION, TY_MODULE, TY_NEVER, TY_OVERLOAD, TY_TYPEVAR, TY_UNION, TY_UNKNOWN, unpack_header }
    compiler.types.stubcat.format --> compiler.types.stubcat.writer { ACCESS_PRIVATE, ACCESS_PROTECTED, ACCESS_PUBLIC, ARCH_CLASS, ARCH_ENUM, ARCH_NONE, ARCH_OBJ, HEADER_SIZE, Header, LIT_BOOL, LIT_INT, LIT_NONE, LIT_STR, MOD_EXTERNAL, MOD_JAC_INTERNAL, MOD_TYPESHED, PM_CLS, PM_COMPTIME, PM_HAS_DEFAULT, PM_SELF, SC_CLASS, SC_FUNCTION, SC_MODULE, SC_OTHER, SH_BUILTIN, SH_DATACLASS, SH_ENUM, SH_NAMEDTUPLE, SH_ROOT, SH_STDLIB, SH_TYPEDDICT, SH_XREF, SYMF_DEFER, SYMF_FINAL, SYMF_HAS_DEFAULT, SYMF_INSTANCE_METHOD, SYMF_NA_ESCAPES, SYMF_NA_REGION_HANDLE, SYMF_NA_STACK_OK, SYMF_PARAM_REBOUND, SYMF_READONLY, TV_CLASS_PARAM, TV_CONTRAVARIANT, TV_COVARIANT, TV_PARAM_SPEC, TV_SELF, TY_ANY, TY_CLASS, TY_ENUM_MEMBER, TY_FUNCTION, TY_MODULE, TY_NEVER, TY_OVERLOAD, TY_TYPEVAR, TY_UNION, TY_UNKNOWN, pack_header, put_ref, put_refs, put_svar, put_uvar }
    compiler.types.stubcat.format --> compiler.types.type_evaluator.TypeEvaluator._is_unbound_method_call { SYMF_INSTANCE_METHOD }
    compiler.types.stubcat.format --> compiler.types.type_evaluator.TypeEvaluator._merge_catalog_field_params { SYMF_DEFER, SYMF_HAS_DEFAULT }
    compiler.types.stubcat.locate --> compiler.driver.ifacecache.IfaceRegistry._pkg_dir { jaclang_pkg_dir }
    compiler.types.stubcat.locate --> compiler.tests.test_stubcat_roundtrip { jaclang_pkg_dir, reset_catalog_cache, typeshed_stdlib_dir }
    compiler.types.stubcat.locate --> compiler.types.stubcat.build { catalog_key, jac_internal_stub_dir, jaclang_pkg_dir, typeshed_stdlib_dir }
    compiler.types.stubcat.modiface --> dist.precompile_bytecode.precompile_unit_context;
    type compiler.types.stubcat.reader --> compiler.driver.compiler { StubCatalog }
    compiler.types.stubcat.reader --> compiler.driver.compiler.JacCompiler.ensure_stub_catalog;
    type compiler.types.stubcat.reader --> compiler.driver.program { StubCatalog }
    compiler.types.stubcat.reader --> compiler.tests.test_stubcat_roundtrip { StubCatalog, open_catalog_file }
    compiler.types.stubcat.reader --> compiler.types.stubcat.build;
    type compiler.types.stubcat.reader --> compiler.types.stubcat.locate { StubCatalog }
    compiler.types.stubcat.reader --> compiler.types.stubcat.locate._open_file { open_catalog_file }
    compiler.types.stubcat.reader --> compiler.types.stubcat.locate._open_region { open_catalog_region }
    compiler.types.stubcat.reader --> compiler.types.stubcat.modiface { StubCatalog }
    type compiler.types.stubcat.reader --> compiler.types.type_evaluator { CatScope, StubCatalog }
    compiler.types.stubcat.reader --> compiler.types.type_evaluator.TypeEvaluator._build_field_params { CatScope }
    compiler.types.stubcat.reader --> compiler.types.type_evaluator.TypeEvaluator._merge_catalog_field_params { CatProvider }
    compiler.types.stubcat.reader --> compiler.types.type_evaluator.TypeEvaluator._metaclass_of { CatScope }
    compiler.types.stubcat.reader --> compiler.types.type_evaluator.TypeEvaluator._scope_has_fields { CatScope }
    compiler.types.stubcat.reader --> compiler.types.types.ClassType.get_class_symbol { CatScope }
    compiler.types.stubcat.reader --> compiler.types.types._class_scope_category { CatScope }
    compiler.types.stubcat.writer --> compiler.types.stubcat.build { CatalogWriter }
    compiler.types.stubcat.format --> compiler.types.stubcat.modiface { IFACE_HASH_LEN }
    compiler.types.stubcat.format --> compiler.types.stubcat.reader { u32_at }
    compiler.types.stubcat.format --> compiler.types.type_evaluator.TypeEvaluator._is_instance_method_member { SYMF_INSTANCE_METHOD }
    compiler.types.stubcat.format --> project.kernel_snapshot.interface_dependencies { MOD_EXTERNAL }
    compiler.types.stubcat.modiface --> compiler.frontend.kernel_host { iface_module, open_module_iface }
    compiler.types.stubcat.modiface --> project.kernel_snapshot.interface_dependencies { open_module_iface }
    compiler.types.stubcat.reader --> compiler.driver.program.JacProgram.load_dependency_module | compiler.types.ct_eval { CatModule }
    compiler.types.stubcat.reader --> compiler.frontend.kernel_host { StubCatalog, open_catalog_region }
    compiler.types.stubcat.reader --> compiler.types.type_evaluator.TypeEvaluator._is_instance_method_member { CatProvider }
    type compiler.types.stubcat.reader --> compiler.frontend.host | project.compiler_host { StubCatalog }
    compiler.types.stubcat.resolver --> compiler.driver.ifacecache | compiler.frontend.kernel_host | compiler.types.stubcat.modiface | compiler.types.stubcat.reader { CatalogResolver }
    compiler.types.stubcat.writer --> dist.precompile_bytecode.precompile_unit_context;
    compiler.types.stubcat.writer --> compiler.driver.ifacecache.IfaceRegistry._encode_iface { IncoherentInterface }
    compiler.types.stubcat.writer --> project.kernel_snapshot.python_interface { IncoherentInterface, build_module_iface }
    compiler.types.stubcat.locate --> compiler.types.stubcat.build._cached_catalog { dev_catalog_path }
    compiler.types.stubcat.locate as locate --> dist.payload.assemble.cached_stubcat;
    compiler.types.stubcat.format --> compiler.types.stubcat.reader { SH_EXTERN }
    compiler.types.stubcat.format --> compiler.types.stubcat.writer { SH_EXTERN }
    compiler.types.stubcat.locate --> project.kernel_snapshot.session_inputs { catalog_origin }
    compiler.types.stubcat.reader --> compiler.driver.unit_products.dependency_span_rows { CatModule }
    compiler.types.stubcat.reader --> compiler.placement.placement_solver._import_source_module { CatModule }
    compiler.types.stubcat.reader --> compiler.types.stubcat.writer.CatalogWriter.encode_symbol { CatProvider }
    compiler.types.stubcat.build --> compiler.types.stubcat.locate.StubcatArtifact.build { build_catalog }
    compiler.types.stubcat.locate --> compiler.driver.compiler.JacCompiler.ensure_stub_catalog { open_catalog }
    compiler.types.stubcat.locate --> compiler.tests.test_stubcat_roundtrip { StubcatArtifact }
    compiler.types.stubcat.locate --> project.kernel_snapshot.require_stub_catalog { reset_catalog_cache }
    compiler.types.stubcat.reader --> compiler.native_bindings.is_owning_scope { CatScope }
    compiler.types.stubcat.reader --> compiler.passes.endpoint_effect_pass.EndpointEffectPass._served_effects { CatModule }
    compiler.types.stubcat.writer --> compiler.driver.unit_products.unit_interface { IncoherentInterface, build_module_iface }
    data.dbcatalog --> cli.commands.db { DbRecord, MAINTENANCE_DB }
    data.dbcatalog --> cli.commands.db._db_drop { is_jac_database }
    data.dbcatalog --> cli.commands.db._db_prune { condemn_abandoned, connect_admin, drop_database, drop_if_still_dead, list_databases, pardon_recovered }
    data.dbcatalog --> cli.commands.db._prune_candidates { holds_no_data }
    data.dbcatalog --> cli.commands.db._runtime_for | data.pgembed { DbKind }
    type data.dbcatalog --> data.pgembed { DbRecord }
    data.dbcatalog --> data.pgembed.PgRuntime._ensure_database { connect_admin, record_database, start_heartbeat }
    data.dbcatalog --> data.pgembed.PgRuntime._reap { condemn_abandoned, drop_if_still_dead, orphan_grace_seconds, pardon_recovered, reclaimable_databases }
    data.dbcatalog --> data.pgembed.PgRuntime._reap_scratch { SCRATCH_PREFIX, list_databases }
    data.dbcatalog --> data.pgembed.PgRuntime._sweep_on_start { connect_admin, drop_database, expired_databases, list_databases }
    data.dbcatalog --> data.pgembed.PgRuntime.databases { connect_admin, list_databases }
    data.dbcatalog --> data.pgembed.PgRuntime.drop_database { connect_admin, drop_database as catalog_drop }
    data.dbcatalog --> server.session { DbKind, MAINTENANCE_DB, SCRATCH_PREFIX, stop_heartbeat }
    data.dbcatalog --> server.session.drop_owned_databases { connect_admin, drop_database, owned_databases }
    data.dbcatalog --> server.session.own_child_databases { process_alive, this_host }
    data.pgembed --> cli.commands.db._catalog_runtime { PgRuntime }
    data.pgembed --> cli.commands.db._runtime_for { PgRuntime }
    data.pgembed --> scale.deploy.database.kubernetes_postgres.KubernetesPostgresProvider.deploy { pg_tuning_settings }
    data.pgembed --> scale.tests.data.test_auth_cutover { PgRuntime }
    data.pgembed --> scale.tests.data.test_pg_stream { PgRuntime }
    data.pgembed --> scale.tests.deploy.test_postgres_predicate_lock_headroom { PG_MAX_CONNECTIONS, PG_MAX_PRED_LOCKS_PER_TXN, PgRuntime, pg_tuning_settings }
    data.pgembed --> scale.tests.server.test_backplane { PgRuntime }
    data.pgembed --> scale.tests.server.test_pg_job_store { PgRuntime }
    data.pgembed --> scale.tests.server.test_registration_limits { PgRuntime }
    data.pgembed --> scale.tests.server.test_scheduler_multipod { PgRuntime }
    data.pgembed --> server.session { PgRuntime }
    data.pgload --> data.dbcatalog.connect_admin { connect }
    data.pgload --> data.dbcatalog.holds_no_data { connect }
    data.pgload --> data.pgembed.PgRuntime._wait_ready { connect }
    data.pgload --> data.store.PgStore._connect { connect as pg_connect }
    data.pgpool --> data.store.PgStore._connect { checkout }
    data.pgpool --> data.store._park_conn { pool_enabled, release }
    data.pgpool --> runtime.runtime.JacRuntime.after_fork_in_child { detach }
    data.pgpool --> server.shared_store._after_fork_in_child { detach }
    data.pgwire --> cli.errmap.humanize_error { PgWireError }
    data.pgwire --> data.store { PgWireError }
    data.pgwire --> data.store.PgStore._run { PgWireError }
    data.pgwire --> scale.server.jobs_ext { PgWireError }
    data.pgwire --> scale.tests.server.test_health_fail_soft { PgWireError }
    data.pgwire --> scale.tests.server.test_scheduler_endpoints { PgWireError }
    data.query_planner --> runtime.runtime.JacGraph.refs { LazyRefs, resolve_query, resolve_query_edges }
    data.schema_rules --> data.serializer.Serializer._deserialize_archetype { ATTIC_KEY, REPAIRS_ATTR, repair_mode }
    data.schema_rules --> data.serializer.Serializer._serialize_attrs { merged_rules_for, repair_mode }
    data.schema_rules --> data.serializer.Serializer.register { collect_rules }
    data.schema_rules --> data.serializer.Serializer.repair { apply_rules, merged_rules_for, repair_mode }
    data.schema_rules --> data.serializer.Serializer.serialize_fields { merged_rules_for, repair_mode }
    data.schema_rules as _rules --> runtime.builtin._get_schema_builder.builder;
    data.serializer --> compiler.tests.test_fixed_width_equivalence { Serializer }
    data.serializer --> compiler.tests.xbackend_equiv.encode_py_wire { Serializer }
    data.serializer --> runtime.builtin._get_archetype_alias.factory.decorator { Serializer }
    data.serializer --> server.endpoints.walkers { Serializer }
    data.serializer --> server.server { Serializer }
    data.serializer --> server.session.Session._load_edges { Serializer }
    data.serializer --> server.session.Session._materialize { Serializer }
    data.serializer --> server.session.Session._serialize { Serializer }
    data.sqlcompile --> data.query_planner { compile_query }
    data.storage --> runtime.runtime.JacPersistence.store { LocalStorage }
    data.storage --> scale.plugin { Storage }
    type data.storage --> scale.runtime.provider { Storage }
    data.storage --> scale.storage.factory.StorageFactory.create { LocalStorage }
    data.storage --> scale.tests.data.test_s3_storage { Storage }
    data.storage --> scale.tests.data.test_storage { LocalStorage }
    data.store --> cli.commands.db { TxnIsolation }
    data.store --> cli.commands.db._open_project_store { PgStore }
    data.store --> cli.commands.db._open_store { PgStore }
    data.store --> cli.errmap.humanize_error { SessionConflictError }
    data.store --> data.dbcatalog { ConnInfo, SCHEMA_STAMP_KEY }
    data.store --> data.pgembed { ConnInfo }
    data.store --> data.sqlcompile { Store }
    data.store --> scale.events.streams.postgres { TxnIsolation }
    data.store --> scale.events.streams.postgres.PgEventStream._ensure_store { PgStore }
    data.store --> scale.memory.context.JScaleExecutionContext.init { PgStore }
    data.store --> scale.scheduler.scheduler { TxnIsolation }
    data.store --> scale.scheduler.scheduler.PgJobStore._quota_connection { PgStore }
    data.store --> scale.tests.data.test_auth_cutover { PgStore }
    data.store --> scale.tests.data.test_pg_stream { PgStore }
    data.store --> scale.tests.server.test_backplane { PgStore }
    data.store --> scale.tests.server.test_pg_job_store { PgStore }
    data.store --> scale.tests.server.test_registration_limits { PgStore }
    data.store --> scale.tests.server.test_scheduler_multipod { PgStore }
    data.store --> server.outbox { OUTBOX_SCHEMA_SQL, PgStore, Store, TxnIsolation }
    data.store --> server.session { AnchorRow, ConnInfo, PgStore, Store, TxnIsolation }
    data.store --> server.shared_store.shared_store { PgStore }
    data.dbcatalog --> data.pgembed.PgRuntime._warn_superseded { list_databases }
    data.type_identity --> data.serializer { TypeResolutionError, UnavailableType, class_facts, register_type, resolution_required, resolve_type, storage_type, type_module }
    data.type_identity --> data.serializer.Serializer.fingerprint { schema_type }
    data.type_identity --> data.sqlcompile.compile_query | server.session._ancestry_of { storage_type }
    data.type_identity --> runtime.prepared.publish { index_application }
    data.type_identity --> server.session.Session._materialize { ForeignType, resolution_scope }
    data.type_identity --> server.session.Session._serialize { storage_type, type_module }
    data.pg_dist --> cli.commands.db._db_fetch { download_dist }
    data.pg_dist --> data.pgembed.PgRuntime._resolve_binaries { postgres_bin_dir }
    data.pgembed --> data.store.PgStore._warn_lock_headroom { predicate_lock_shortfall }
    data.pgembed --> scale.tests.deploy.test_postgres_predicate_lock_headroom { predicate_lock_shortfall }
    data.serializer --> server.session { frozen_fields }
    data.serializer --> server.session.Session._unflushed { Serializer }
    data.storage.local_storage --> data.storage { LocalStorage }
    data.storage.local_storage --> scale.tests.data.test_s3_storage { LocalStorage }
    data.storage.storage --> data.storage { Storage }
    data.storage.storage --> data.storage.local_storage { Storage }
    data.storage.storage --> scale.storage.bucket_storage { Storage }
    data.storage.storage --> scale.storage.factory { Storage }
    dist.fused_binary --> cli.commands.cache._live_keys { running_runtime_entries }
    dist.fused_binary --> cli.commands.project._bundle_binary { append_overlay, has_runtime }
    dist.fused_binary --> client.targets.desktop.desktop_build._bundle_runtime { graft_runtime }
    dist.jab --> cli.cli_boot._run_bundled_app { materialize_jab_bytes }
    dist.jab --> cli.commands.execution._run_jab { materialize_jab }
    dist.jab --> cli.commands.execution.run_jab_image { jab_app_meta }
    dist.jab --> client.targets.desktop.native.host_boot.resolve_program { jab_app_meta, materialize_jab }
    dist.jab_vendor --> dist.jab { activate_vendored }
    dist.jab_vendor --> dist.seal.vendor_jab_deps { download_wheels, wheels_dir, write_vendor_manifest }
    dist.jab_vendor --> scale.tests.microservices.test_fat_bundle { WheelTarget, download_wheels }
    dist.jab_vendor --> scale.utils.vendor_wheels { WheelTarget, download_wheels, wheels_dir, write_vendor_manifest }
    dist.native_product --> dist.publish.runtime_vendor._compile_runtime_module { write_native_product }
    dist.native_product --> dist.source.project._write_application { write_native_product }
    dist.native_product --> dist.source.project.export_project { write_native_product }
    dist.precompile_bytecode --> cli.commands.precompile.precompile { run_precompile }
    dist.precompile_bytecode --> dist.seal.resolve_entry_file { bundle_app }
    dist.precompile_bytecode as precompiler --> scale.tests.microservices.test_app_precompile;
    dist.precompile_bytecode --> scale.tests.microservices.test_app_precompile { main as seal_main, placement_facts_map, sealable_sources }
    dist.seal --> cli.commands.project { build_jab, make_sealed_image as _make_sealed_image }
    dist.seal --> client.targets.desktop.desktop_build.stage_program { build_jab }
    dist.archive --> dist.seal.build_jab | packages.artifact { tar_gz_dir }
    dist.archive --> packages.store | packages.templates | packages.verify { extract_tar_gz }
    dist.archive --> scale.injector.binary.pack_binary_bytes | scale.tests.microservices.test_bundle_jacignore { open_det_tar }
    dist.archive --> scale.injector.bundle { det_tar_member, open_det_tar }
    dist.jab --> dist.seal.build_jab { jab_app_meta }
    dist.sanitize --> dist.seal.make_sealed_image | packages.artifact { sanitize_shipped_tree }
    dist.sanitize --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._build_client_bundle | scale.injector.bundle | scale.tests.microservices.test_app_precompile | scale.tests.microservices.test_bundle_jacignore | scale.tests.microservices.test_pvc_injector { sanitized_jac_toml }
    dist.sanitize --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._check_pod_config_resolves { sanitized_jac_toml }
    dist.fused_binary --> client.targets.desktop.desktop_build._jac_bin { jac_binary }
    dist.fused_binary --> compiler.types.stubcat.locate.StubcatArtifact.probe_kit { running_executable }
    dist.fused_binary --> compiler.types.stubcat.locate.StubcatArtifact.probe_sealed { running_executable }
    dist.fused_binary --> compiler.types.stubcat.locate._region_probe { stubcat_region }
    dist.fused_binary --> scale.runtime.context.util.jac_executable { jac_binary }
    dist.precompile_bytecode --> dist.precompiled.PrecompiledArtifact.build { run_precompile }
    dist.precompile_bytecode --> dist.precompiled.bundle_misses { sealable_sources }
    dist.publish --> dist.publish.builder._backend_source { wheel_archive }
    dist.payload.assemble --> dist.payload.cli { MkPayloadOpts, mk_payload }
    dist.payload.assemble --> dist.payload.cli.dispatch { resolve_python, run_stubcat }
    dist.payload.cli --> dist.payload { main }
    dist.payload.fetch --> dist.payload.assemble { TYPESHED_VENDOR, fetch_typeshed }
    dist.payload.fetch --> dist.payload.cli { fetch_bun, fetch_llvm, fetch_typeshed, typeshed_sha }
    dist.payload.fsutil --> dist.payload.assemble { PayloadDie, clone_env, copy_file, copy_into, copy_tree, delete_file, delete_tree, die, file_exists, host_os_arch, log, make_dirs, read_bytes, run_child, sha256_hex, skip_jaclang, skip_none, skip_site_template, skip_stage_site, source_file_mode, strip_best_effort, toml_string, walk_sorted, write_bytes, write_text }
    dist.payload.fsutil --> dist.payload.cli { PayloadDie, die }
    dist.payload.fsutil --> dist.payload.fetch { PayloadDie, copy_file, copy_tree, delete_tree, die, extract_tar, file_exists, find_sum_line, host_os_arch, log, make_dirs, rd_u16, rd_u32, read_trimmed, sha256_hex, skip_typeshed_tests, write_bytes, write_text }
    dist.payload.fsutil --> dist.payload.pack { die, read_bytes, sha256_hex, strip_best_effort }
    dist.payload.fsutil --> dist.payload.pins { die }
    dist.payload.fsutil --> dist.payload.vendor { clone_env, copy_file, delete_file, delete_tree, die, file_exists, log, make_dirs, mtime_ns, read_bytes, run_child, sha256_hex, walk_sorted, write_text }
    dist.payload.pack --> dist.payload.cli { pack }
    dist.payload.pins --> dist.payload.assemble { py_ver }
    dist.payload.pins --> dist.payload.cli { host_py_minor, py_ver }
    dist.payload.pins --> dist.payload.fetch { LlvmSlice, llvm_release, pins }
    dist.payload.vendor --> dist.payload.assemble { MUSL_ARTIFACTS }
    dist.payload.vendor --> dist.payload.cli { build_musl, build_wasm_libc }
    dist.payload.fetch --> client.js_runtime.BunArtifact.build { fetch_bun }
    dist.payload.fetch --> compiler.types.stubcat.locate.TypeshedArtifact.build { fetch_typeshed }
    dist.publish.builder --> cli.commands.project._bundle_wheel { WheelBuilder }
    dist.publish.builder --> cli.commands.project.install { WheelBuilder }
    dist.publish.builder --> dist.publish { WheelBuilder }
    dist.publish.dts --> dist.publish.npm_sources { dts_for_module }
    dist.publish.jsdoc --> dist.publish.dts { jac_type_to_ts }
    dist.publish.jsdoc --> dist.publish.npm_sources { inject_jsdoc, jsdoc_for_module }
    dist.publish.metadata --> dist.publish { generate_metadata, normalize_package_name }
    dist.publish.metadata --> dist.publish.builder { generate_metadata, generate_pyproject_toml }
    dist.publish.metadata --> dist.publish.package_json { normalize_package_name }
    dist.publish.metadata --> dist.publish.wheel_meta { normalize_package_name }
    dist.publish.npm_builder --> cli.commands.project._bundle_npm { NpmBuilder }
    dist.publish.npm_sources --> cli.commands.project._bundle_npm { NpmBoundaryError }
    dist.publish.npm_sources --> dist.publish.npm_builder { collect_npm_sources, resolve_npm_entry, runtime_pkg_name }
    dist.publish.npm_tarball --> dist.publish.npm_builder { pack_tarball }
    dist.publish.npm_tarball --> dist.publish.runtime_npm { pack_tarball }
    dist.publish.package_json --> dist.publish.npm_builder { generate_package_json, npm_tarball_filename }
    dist.publish.py_imports --> dist.publish.builder { rewrite_imports, wheel_module_name }
    dist.publish.record --> dist.publish.builder { RecordEntry, generate_record, record_entry_from_bytes }
    dist.publish.runtime_npm --> cli.commands.project._bundle_npm_runtime { build_runtime_to, runtime_pkg_name }
    dist.publish.runtime_npm --> dist.publish.npm_sources { runtime_api_names }
    dist.publish.runtime_vendor --> dist.publish.builder { build_runtime_closure, scan_jaclang_imports }
    dist.publish.runtime_vendor --> dist.source.project.export_project { vendor_runtime }
    dist.publish.sources --> dist.publish.builder { SourceFile, collect_source_files, read_source_file }
    dist.publish.sources --> dist.publish.npm_sources { EXCLUDED_DIRS }
    dist.publish.sources --> dist.source.project._copy_resources { EXCLUDED_DIRS, EXCLUDED_SUFFIXES }
    dist.publish.wheel_meta --> dist.publish { wheel_filename }
    dist.publish.wheel_meta --> dist.publish.builder { dist_info_dirname, generate_entry_points, generate_wheel_file, sdist_filename, wheel_filename }
    dist.publish.wheel_archive --> dist.publish.builder { BUILD_DATA_FILE, wheel_bytes }
    dist.publish.wheel_archive --> dist.publish.record { record_hash, record_text }
    dist.source.client --> dist.source.project._write_application { write_client }
    dist.source.project --> cli.commands.build._build_app { export_project }
    jac0core.cache_paths --> cache.home { get_cache_home }
    jac0core.cache_paths --> compiler.backends.es.client_kernel_cache._cache_dir { get_jir_cache_dir }
    jac0core.cache_paths --> compiler.backends.native.elf_linker { atomic_write }
    jac0core.cache_paths --> compiler.backends.native.link_plan { atomic_write }
    jac0core.cache_paths --> compiler.backends.native.macho_linker { atomic_write }
    jac0core.cache_paths --> compiler.backends.native.pe_linker { atomic_write }
    jac0core.cache_paths --> compiler.driver.jir { FileLock, atomic_write }
    jac0core.cache_paths --> compiler.driver.jir.get_jir_cache_dir { get_jir_cache_dir as _root }
    jac0core.ext_registry --> cli.commands.analysis._drop_covered_annexes { is_annex }
    jac0core.ext_registry --> cli.commands.cli_helpers { base_stem, is_jac, is_python }
    jac0core.ext_registry --> cli.commands.execution._jab_native_bin { base_stem }
    jac0core.ext_registry --> cli.commands.native_build.native_build { base_stem, is_jac, is_retired_native_marker }
    jac0core.ext_registry --> client.jac_client_compiler { ANNEX_SUFFIXES }
    jac0core.ext_registry --> client.jac_client_compiler.JacClientCompiler._native_variant { base_stem }
    jac0core.ext_registry --> client.targets.client_dev_common.dev_proxy_paths { base_stem }
    jac0core.ext_registry --> compiler.driver.application._semantic_metadata { base_stem }
    jac0core.ext_registry --> compiler.driver.bccache { ANNEX_FOLDER, MODULE_SUFFIXES }
    jac0core.ext_registry --> compiler.tools.code_intel { ANNEX_FOLDER, ANNEX_SUFFIXES, IMPL_SUFFIX, is_annex }
    jac0core.ext_registry --> dist.publish.builder { is_annex }
    jac0core.ext_registry --> dist.seal.bake_native_payloads { base_stem }
    jac0core.ext_registry --> project.kinds { base_stem }
    jac0core.ext_registry --> project.modresolver { MODULE_SUFFIXES, is_jac_namespace_package, language_of }
    jac0core.ext_registry --> project.placement { base_stem }
    jac0core.ext_registry --> runtime.prepared { base_stem }
    jac0core.ext_registry --> runtime.prepared.semantic_for_scope { base_stem }
    jac0core.ext_registry --> runtime.runtime.JacModule.impl_patch_filename.decorator { is_jac }
    jac0core.ext_registry --> scale.server.inprocess { base_stem }
    jac0core.ext_registry --> server.hmr.HotReloader._dispatch_change { is_impl }
    jac0core.ext_registry --> server.hmr.HotReloader._get_js_filename { base_stem }
    jac0core.ext_registry --> server.hmr.HotReloader._path_to_module { base_stem }
    jac0core.ext_registry --> testing.runner.run_test { base_stem, is_annex }
    jac0core.ext_registry --> testing.test { strip_suffix }
    jac0core.ext_registry --> testing.test_runner._is_named_test_file { is_jac, is_test }
    jac0core.ext_registry --> testing.test_runner._iter_candidate_files { is_impl, is_jac }
    jac0core.ext_registry --> testing.test_runner._suite_source { is_test }
    jac0core.ext_registry --> testing.test_runner.discover { is_jac }
    jac0core.ext_registry --> testing.test_runner.run_file { base_stem }
    jac0core.sealed --> compiler.driver.application._prepare_sealed { image_for_bundle_dir, register_image }
    jac0core.sealed --> dist.jab { MANIFEST_NAME, image_for_bundle_dir, register_image }
    jac0core.sealed --> dist.precompile_bytecode { HEADER_SIZE as SEALED_HEADER_SIZE, JIR_FORMAT_VERSION as SEALED_JIR_FORMAT_VERSION, MANIFEST_FORMAT, MANIFEST_NAME, PRECOMPILE_SENTINEL as SEALED_SENTINEL, SECTIONS_MAGIC as SEALED_SECTIONS_MAGIC, SEC_BYTECODE as SEALED_SEC_BYTECODE, SEC_DEBUG_SRC as SEALED_SEC_DEBUG_SRC, SEC_NIFACE as SEALED_SEC_NIFACE, SEC_NOBJ as SEALED_SEC_NOBJ }
    jac0core.sealed --> dist.seal.vendor_jab_deps { python_tag }
    jac0core.sealed --> scale.utils.vendor_wheels { python_tag }
    jac0core.sealed --> server.sealed_serve { MANIFEST_NAME }
    jac0core.stubcat_hook --> compiler.driver.compiler.JacCompiler.stub_catalog { active }
    jac0core.stubcat_hook --> compiler.types.stubcat.locate._publish { set_active }
    jac0core.stubcat_hook --> compiler.types.stubcat.locate.reset_catalog_cache { set_active }
    jac0core.stubcat_hook --> project.modresolver._candidate_from_stub_catalog { active }
    jac0core.stubcat_hook --> project.modresolver._stub_catalog_active { active }
    jac0core.cache_paths --> client.targets.desktop.desktop_build._native_build_cef | client.targets.node_tooling_common.run_manifest_install | client.targets.react_native.build.run_gradle_assemble | toolchains.android | toolchains.apple | toolchains.c_backend | toolchains.cef | toolchains.desktop | toolchains.store { FileLock }
    jac0core.cache_paths --> compiler.types.stubcat.build | scale.injector.binary { atomic_write }
    jac0core.ext_registry --> compiler.driver.bccache.host_layout_tables { ANNEX_FOLDER, INIT_FILES, JAC_SUFFIX, MODULE_SUFFIXES, RETIRED_CLIENT_SUFFIX, RETIRED_NATIVE_SUFFIX, STEM_REKEY_SUFFIXES, _JS_SUFFIXES, _PY_SUFFIXES }
    jac0core.ext_registry --> compiler.driver.pipeline_runner.compile_application { is_annex }
    jac0core.stubcat_hook --> project.compiler_host.ProjectHost.has_active_stub_catalog { active }
    jac0core.cache_paths --> packages.sources.checkout | packages.store.materialize { FileLock }
    jac0core.ext_registry --> testing.cl_test_runner.module_entry_for { is_annex }
    jac0core.ext_registry --> project.kernel_snapshot.KernelSnapshot.emits { is_annex }
    jac0core.stubcat_hook --> project.kernel_snapshot.session_inputs { active }
    jac0core.artifact_registry --> artifacts.router._BuildingSpan.__enter__ { begin }
    jac0core.artifact_registry --> artifacts.router._BuildingSpan.__exit__ { end }
    jac0core.artifact_registry --> artifacts.router.artifact_named { ARTIFACTS }
    jac0core.artifact_registry --> artifacts.router.building_now { building as marked }
    jac0core.artifact_registry --> artifacts.router.names { ARTIFACTS }
    jac0core.artifact_registry --> artifacts.router.resolve { resolution_in_flight }
    jac0core.artifact_registry --> compiler.driver.compiler.JacCompiler.ensure_stub_catalog { resolution_in_flight }
    jac0core.artifact_registry --> compiler.native_compiler.ensure_loaded { resolution_in_flight }
    jac0core.cache_paths --> artifacts.router.publish { FileLock, atomic_write }
    jac0core.cache_paths --> client.js_runtime.JsEngineArtifact.build { atomic_write }
    jac0core.cache_paths --> client.js_runtime.write_bun_record { atomic_write }
    jac0core.cache_paths --> compiler.backends.native.llvm.shim_path.write_shim_record { atomic_write }
    jac0core.cache_paths --> data.pg_dist.download_dist { FileLock }
    jac0core.cache_paths --> project.kernel_snapshot.build_stub_catalog { FileLock }
    jac0core.ext_registry --> server.watcher.JacFileWatcher._beside_watched_file { is_annex_path_of }
    jac0core.ext_registry --> server.watcher.JacFileWatcher._foreign_shared_annex { ANNEX_FOLDER, JAC_SUFFIX, is_annex_path_of, shared_annex_folder }
    jac0core.ext_registry --> server.watcher.annex_folders_of { ANNEX_FOLDER, JAC_SUFFIX, shared_annex_folder }
    jac0core.handoff --> cli.cli.start_cli { handoff }
    jac0core.handoff --> cli.manifest_route.resolve_cli_version { handoff }
    jac0core.handoff --> client.js_runtime.ensure_node_link { process_executable }
    jac0core.handoff --> client.targets.desktop.native.host_boot.host_executable { process_executable }
    jac0core.handoff --> compiler.driver.jir._handoff { handoff }
    jac0core.handoff --> compiler.driver.jir.require_exact_compiler_products { update_handoff }
    jac0core.handoff --> compiler.driver.jir.set_cache_mode { update_handoff }
    jac0core.handoff --> dist.fused_binary.running_executable { process_executable }
    jac0core.handoff --> jac0core.artifact_registry._marks { handoff }
    jac0core.handoff --> jac0core.artifact_registry._record { update_handoff }
    type jac0core.sealed --> artifacts.kit { SealedImage }
    jac0core.sealed --> artifacts.kit._find_kit { load_image }
    jac0core.stubcat_hook --> compiler.types.stubcat.locate.open_catalog { catalog_disabled }
    jac0core.stubcat_hook --> project.kernel_snapshot.require_stub_catalog { catalog_disabled }
    lib.jaclib as _jaclib --> lib;
    include lib.jaclib --> lib;
    lsp.protocol.server --> lsp.server.engine { LanguageServer }
    lsp.protocol.types --> lsp.protocol.server { Diagnostic, DidChangeTextDocumentParams, DidCloseTextDocumentParams, DidOpenTextDocumentParams, EXIT, INITIALIZE, INITIALIZED, METHOD_TO_PARAMS, Position, PositionEncodingKind, Range, SHUTDOWN, TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_DID_CLOSE, TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_PUBLISH_DIAGNOSTICS, TextDocumentContentChangeEvent, TextDocumentContentChangeEvent_Type1, TextDocumentItem, TextDocumentSyncKind, VersionedTextDocumentIdentifier, WINDOW_LOG_MESSAGE, WINDOW_SHOW_MESSAGE, WORKSPACE_SEMANTIC_TOKENS_REFRESH }
    lsp.protocol.types as lspt --> lsp.server.engine;
    lsp.protocol.types as lspt --> lsp.server.sem_manager;
    lsp.protocol.types as lspt --> lsp.server.server;
    lsp.protocol.types as lspt --> lsp.server.utils;
    lsp.server.engine --> lsp.server.server { JacLangServer }
    lsp.server.module_manager --> lsp.server.engine { ModuleManager }
    lsp.server.rwlock --> lsp.server.engine { ReadWriteLock }
    lsp.server.sem_manager --> lsp.server.engine { SemTokManager }
    lsp.server.sem_manager --> lsp.server.module_manager { SemTokManager }
    lsp.server.server --> cli.commands.tools.lsp { run_lang_server }
    lsp.server.utils --> lsp.server.engine { doc_of_sym, get_completion_items }
    project.textio --> project.compiler_host._git_ignored_under { drop_git_ignored }
    project.app_kinds --> dist.seal.build_serve_manifest { kind_has_server }
    project.app_kinds --> dist.source.project.export_project { kind_has_client, kind_has_server }
    project.app_kinds --> project.apps.AppConfig.entry_path { kind_entry }
    project.app_kinds --> project.apps.AppConfig.ui { kind_ui }
    project.app_kinds --> project.apps.parse_apps { KIND_SPECS }
    project.app_kinds --> project.kinds { KIND_SPECS, KindSpec, MOBILE_PLATFORMS, UI_DOM, UI_MOBUI, VALID_KINDS, is_valid_kind, kind_entry, kind_has_client, kind_is_mobui, kind_spec, kind_ui }
    project.app_kinds --> project.workspace { UI_MOBUI, kind_codespace, kind_entry, kind_has_server, kind_ui }
    project.app_kinds --> runtime.source_app.main { kind_has_server }
    type project.apps --> client.cli { AppConfig }
    type project.apps --> client.targets.registry { AppConfig }
    type project.apps --> dist.seal { AppConfig }
    type project.apps --> project.client_paths { AppConfig }
    project.apps --> project.config { AppConfig, implicit_app, parse_apps }
    project.apps --> project.config._parse_toml_data { validate_entry_point }
    project.apps --> project.kinds { AppConfig, implicit_app }
    project.apps --> project.template_loader.load_template_from_directory { parse_apps }
    project.apps --> project.template_loader.scaffold_app { APP_TABLE_KEYS, parse_apps, validate_app_name }
    project.apps --> project.workspace._build_workspace { parse_apps, resolve_entry_path }
    project.apps --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._client_entry { resolve_entry_path }
    project.apps --> scale.injector.bundle._entry_module_spec { resolve_entry_path }
    type project.apps --> scale.runtime.fleet { AppConfig }
    type project.apps --> server.assembly { AppConfig }
    project.capabilities --> byllm._optdeps.pillow.open_image { require_optional }
    project.capabilities --> byllm._optdeps.pydantic.TypeAdapter { require_optional }
    project.capabilities --> byllm.llm { require_optional }
    project.capabilities --> project.providers.capability_dependencies { DEPLOY, RUNTIME, byllm_intent_capabilities, command_capabilities, derive_capabilities, get_capability_registry, resolve_closure, scale_intent_from_config }
    project.capabilities --> scale._optdeps.optional_deps { missing_capability_error }
    project.capabilities --> scale.deploy.target.factory { ensure_global_capability, missing_capability_dists }
    project.capabilities --> scale.tests.deploy.test_dry_run_purity { CAPABILITY_SPECS }
    project.client_paths --> client.artifact.client_output_dir { client_app_dir_for }
    project.client_paths --> client.config_loader.JacClientConfig.get_assets_config { client_assets_config }
    project.client_paths --> client.config_loader.JacClientConfig.get_assets_dir { client_assets_dir }
    project.client_paths --> client.jac_client_compiler.JacClientCompiler._app_root { client_app_root }
    project.client_paths --> client.jac_client_compiler.JacClientCompiler._client_app_dir { client_workspace_app }
    project.client_paths --> client.serving.JacClient.render_page { client_workspace_app }
    project.client_paths --> client.targets.desktop.desktop_build.stage_program { client_assets_dir }
    project.client_paths --> client.targets.desktop.desktop_target.DesktopTarget.out_dir_for { client_app_dir_for }
    project.client_paths --> client.targets.react_native.scaffold._project_native_deps { client_workspace_app }
    project.client_paths --> client.vite_bundler.ViteBundler._client_app_dir { client_workspace_app }
    project.client_paths --> dist.seal.ensure_client_dist { client_app_dir_for }
    project.client_paths --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._client_dist_candidates { client_workspace_app }
    project.client_paths --> server.server.JacAPIServer._ensure_client_bundle { client_app_dir_for }
    project.client_paths --> server.static_files { client_app_dir_for, client_app_root, client_assets_config, client_assets_dir }
    project.config --> byllm.mtir.MTRuntime.factory { find_project_root }
    project.config --> cache.registry.project_bucket { get_config }
    project.config --> cli.commands.analysis._configured_check_excludes { get_config }
    project.config --> cli.commands.analysis._format_single_file_worker { get_config_for_path }
    project.config --> cli.commands.analysis._is_project_wide_run { get_config }
    project.config --> cli.commands.analysis.check { get_config }
    project.config --> cli.commands.analysis.format { get_config }
    project.config --> cli.commands.analysis.precommit { get_config }
    project.config --> cli.commands.analysis.test { get_config }
    project.config --> cli.commands.architecture { get_config }
    type project.config --> cli.commands.build { AppConfig }
    project.config --> cli.commands.build.build { get_config }
    project.config --> cli.commands.code { find_project_root }
    project.config --> cli.commands.config { JacConfig }
    project.config --> cli.commands.config._config_path { find_project_root, get_config }
    project.config --> cli.commands.config._config_set { JacConfig, find_project_root }
    project.config --> cli.commands.config._config_unset { find_project_root }
    project.config --> cli.commands.config._get_group_defaults { BuildConfig, CacheConfig, CheckConfig, DotConfig, EnvironmentConfig, FormatConfig, ProjectConfig, RunConfig, ServeConfig, TestConfig }
    project.config --> cli.commands.config._output_toml { toml_value }
    project.config --> cli.commands.config.config { JacConfig, get_config }
    type project.config --> cli.commands.execution { AppConfig, JacConfig }
    project.config --> cli.commands.execution._default_codespace_is_native { PlacementConfig, get_config }
    project.config --> cli.commands.execution._discover_config_from_file { JacConfig, get_config, project_scope_is_pinned, set_config }
    project.config --> cli.commands.execution._ensure_watchdog_installed { get_config }
    project.config --> cli.commands.execution._exec_file { get_config }
    project.config --> cli.commands.execution._load_cwd_config { get_config }
    project.config --> cli.commands.execution._pin_run_scope { JacConfig, get_config, pin_project_scope }
    project.config --> cli.commands.execution._resolve_target { get_config }
    project.config --> cli.commands.execution._run_node_tool { get_config }
    project.config --> cli.commands.execution._tool_tiers { get_config }
    project.config --> cli.commands.execution.run_jab_image { get_config_for_path }
    project.config --> cli.commands.execution.serve { get_config }
    project.config --> cli.commands.execution.x { get_config }
    project.config --> cli.commands.fix._append_app_table { _toml_append_section }
    project.config --> cli.commands.fix._ensure_workspace { JacConfig }
    project.config --> cli.commands.mcp.mcp_cmd { get_config }
    type project.config --> cli.commands.project { JacConfig }
    project.config --> cli.commands.project._bootstrap_project_deps { get_config, set_config }
    project.config --> cli.commands.project._create_app { find_project_root }
    project.config --> cli.commands.project._create_body { find_project_root }
    project.config --> cli.commands.project.bundle { get_config }
    project.config --> cli.commands.project.clean { get_config }
    project.config --> cli.commands.project.deps { get_config }
    project.config --> cli.commands.project.install { get_config }
    project.config --> cli.commands.project.remove { get_config }
    project.config --> cli.commands.project.script { get_config }
    project.config --> cli.commands.project.update { get_config }
    project.config --> cli.dispatch._apply_profile { get_config }
    project.config --> cli.dispatch._discover_project_config { get_config }
    project.config --> cli.mcp.mode { JacConfig, get_config, set_config }
    project.config --> cli.shadcn.cli.retheme { get_config }
    project.config --> cli.shadcn.cli.run_shadcn_add { get_config }
    project.config --> cli.shadcn.cli.run_shadcn_remove { get_config }
    project.config --> client.artifact.client_output_dir { get_config_for_path }
    project.config --> client.asset_processor { get_config }
    project.config --> client.cli { JacConfig }
    project.config --> client.cli.get_config { get_config as _get_config }
    project.config --> client.client_deps._resolve_client_framework { get_config }
    project.config --> client.client_diagnostics.is_debug_mode { JacConfig }
    project.config --> client.config_loader { JacConfig }
    project.config --> client.jac_client_compiler.JacClientCompiler._app_root { get_config }
    project.config --> client.jac_client_compiler.JacClientCompiler._client_app_dir { get_config }
    project.config --> client.jac_client_compiler.JacClientCompiler._get_client_dir { get_config }
    project.config --> client.npm_provider { JacConfig }
    project.config --> client.serving { get_config_for_path }
    project.config --> client.targets.desktop._dev_launch { get_config }
    project.config --> client.targets.desktop.desktop_build.stage_program { get_config_for_dir }
    project.config --> client.targets.desktop.desktop_target.DesktopTarget.out_dir_for { get_config_for_dir }
    project.config --> client.targets.pwa_build { get_config }
    project.config --> client.targets.react_native.scaffold { JacConfig }
    project.config --> client.targets.react_native.scaffold._project_native_deps { get_config_for_dir }
    project.config --> client.targets.registry.target_for_app { get_config }
    project.config --> client.targets.web_target._get_app_meta_data { get_config }
    project.config --> client.vite_bundler.ViteBundler._client_app_dir { get_config }
    project.config --> client.vite_bundler.ViteBundler._get_client_dir { get_config }
    project.config --> client.vite_bundler.ViteBundler.init { find_project_root }
    project.config --> client.vite_bundler._dev_head_scripts { get_config }
    project.config --> client.vite_client_bundle.make_client_bundle_builder { find_project_root }
    project.config --> dist.precompile_bytecode.app_metadata { get_config_for_path }
    project.config --> dist.precompile_bytecode.precompile_context { get_config_for_path }
    project.config --> dist.publish.builder { JacConfig }
    project.config --> dist.publish.metadata { JacConfig, PersonConfig }
    project.config --> dist.publish.npm_builder { JacConfig }
    project.config --> dist.publish.npm_sources { JacConfig }
    project.config --> dist.publish.package_json { JacConfig, PersonConfig }
    project.config --> dist.publish.sources { JacConfig }
    project.config --> dist.publish.wheel_meta { JacConfig }
    project.config --> dist.seal.build_serve_manifest { get_config_for_path }
    project.config --> dist.source.project { JacConfig }
    project.config --> project.capabilities { JacConfig }
    type project.config --> project.client_paths { JacConfig }
    project.config --> project.kinds { JacConfig }
    project.config --> project.modresolver._get_path_aliases { get_config }
    project.config --> project.modresolver._resolve_path_alias { get_config }
    project.config --> project.plugin_config { JacConfig, find_project_root, get_config_for_path }
    project.config --> project.providers { JacConfig }
    project.config --> project.pyvenv { JacConfig }
    project.config --> project.pyvenv.add_venv_to_path { get_config }
    project.config --> project.pyvenv.is_venv_in_path { get_config }
    project.config --> project.pyvenv.remove_venv_from_path { get_config }
    project.config --> project.template_loader { JacConfig }
    project.config --> project.template_loader._append_overlay_tables { _toml_append_section }
    project.config --> project.template_loader.migrate_implicit_app { _toml_append_section, _toml_delete_key, _toml_insert_key, toml_value }
    project.config --> project.template_loader.scaffold_app { _toml_append_section }
    project.config --> project.tool_paths { JacConfig, get_config }
    project.config --> runtime.graph_utils.get_name { get_config }
    project.config --> runtime.runtime.JacRuntime.reset_process_state { set_config }
    project.config --> runtime.source_app.main { JacConfig, set_config }
    project.config --> scale.config.app_config { get_config_for_dir }
    project.config --> scale.config.dev_config.resolve_dev_channel { get_config_for_path }
    project.config --> scale.config.dev_config.resolve_experimental_pr { get_config_for_path }
    project.config --> scale.config.dev_config.resolve_pinned_spec { get_config_for_path }
    project.config --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._check_deploy_settings_resolve { get_config_for_path, report_env_findings }
    project.config --> scale.injector.binary.deploy_generation_refusal { JacConfig, find_project_root }
    project.config --> scale.injector.binary.resolve_pinned_version { JacConfig, find_project_root }
    project.config --> scale.injector.bundle._project_config { get_config_for_path }
    project.config --> scale.injector.bundle._resolved_python_specs { JacConfig }
    project.config --> scale.injector.bundle.fat_bundle_setting { get_config_for_path }
    project.config --> scale.injector.bundle.seal_timeout_setting { get_config_for_path }
    project.config --> scale.injector.bundle.unresolved_toml_references { resolve_env_refs }
    project.config --> scale.plugin._resolve_deploy_target { get_config }
    project.config --> scale.plugin.scale_local_serve { get_config }
    project.config --> scale.runtime.fleet.fleet_member_names { get_config, get_config_for_dir }
    project.config --> scale.runtime.realizer.kubernetes_realizer.KubernetesRealizer._resolve_fleet { get_config_for_dir }
    project.config --> scale.server.inprocess.prepare_inprocess_runtime { get_config_for_dir }
    project.config --> scale.storage.factory { get_config }
    project.config --> scale.tests.apps.test_app_scale_overrides { JacConfig, get_config, get_explicit_config, set_config }
    project.config --> scale.tests.apps.test_fleet_from_apps { JacConfig }
    project.config --> scale.tests.data.test_gcs_storage { JacConfig }
    project.config --> scale.tests.data.test_s3_storage { JacConfig }
    project.config --> scale.tests.deploy.test_deploy_banner { JacConfig }
    project.config --> scale.tests.deploy.test_dry_run_purity { JacConfig }
    project.config --> scale.tests.deploy.test_version_pin { JacConfig }
    project.config --> scale.tests.microservices.test_app_precompile { get_config_for_path }
    project.config --> scale.tests.misc.test_config_validation { JacConfig }
    project.config --> scale.tests.server.test_examples { find_project_root }
    project.config --> scale.tests.server.test_host_serving { set_config }
    project.config --> scale.tests.server.test_served_app_route { set_config }
    project.config --> scale.utils.vendor_wheels { JacConfig }
    project.config --> server.endpoints.colocated { get_config }
    project.config --> server.endpoints.colocated.served_app_route { get_config_for_dir }
    project.config --> server.endpoints.pages { get_config }
    project.config --> server.endpoints.pages.register_diagnostics_endpoints.client_error { get_config }
    project.config --> server.hmr.HotReloader._reload_server_module { get_config_for_dir }
    project.config --> server.server.JacAPIServer._ensure_client_bundle { get_config }
    project.config --> server.server.JacAPIServer.build_app { JacConfig }
    project.config --> server.server._occ_policy { get_config }
    project.config --> server.server.print_endpoint_docs { get_config }
    project.config --> server.settings { JacConfig, ServeConfig }
    project.config --> server.settings.secret_home { find_project_root }
    project.config --> server.static_files { find_project_root, get_config, get_config_for_dir }
    project.config --> server.sv_client._read_cache_enabled { get_config }
    project.config --> testing.test_runner._fresh_jac_state { get_explicit_config, set_config }
    project.config --> testing.testing { JacConfig }
    type project.config --> testing.testing { JacConfig }
    project.config --> testing.testing.JacTestClient._ensure_initialized { get_config, set_config }
    project.config_schema --> project.plugin_config.PluginConfigBase._validate_layer { report_schema_findings, validate_against_schema }
    project.config_schema --> scale.config.config_loader.app_scale_overrides { report_schema_findings }
    project.config_schema --> scale.config.validation { report_schema_findings, validate_against_schema }
    project.config_schema --> scale.tests.misc.test_config_validation { report_schema_findings, schema_strict_enabled }
    project.kinds --> cli.commands.build._build_app { kind_has_client, plan_app_run }
    project.kinds --> cli.commands.execution | scale.plugin { RunPlan }
    project.kinds --> cli.commands.execution._app_serves { kind_spec }
    project.kinds --> cli.commands.execution._exec_file { resolve_app_kind }
    project.kinds --> cli.commands.execution._resolve_plan { plan_app_run }
    project.kinds --> cli.commands.execution._serve_fleet { plan_app_run }
    project.kinds --> cli.commands.execution._workspace_plans { plan_app_run, plan_workspace }
    project.kinds --> cli.commands.project._create_app { VALID_KINDS, is_valid_kind }
    project.kinds --> cli.commands.project._create_body { VALID_KINDS, is_valid_kind }
    project.kinds --> cli.commands.project._run_blurb { VALID_KINDS }
    project.kinds --> client.cli.run_client_start { kind_has_client }
    project.kinds --> client.cli.setup { kind_has_client }
    project.kinds --> client.npm_provider._app_wants_client { kind_has_client }
    project.kinds --> dist.precompile_bytecode.app_metadata { resolve_app_kind, resolve_entry }
    project.kinds --> project.config.JacConfig.resolved_kind { resolve_app_kind, resolve_entry }
    project.kinds --> project.config.JacConfig.serving_apps { kind_spec }
    project.kinds --> project.providers.capability_dependencies { plan_app_run }
    project.kinds --> project.template_loader.migrate_implicit_app { kind_entry }
    project.kinds --> project.template_loader.scaffold_app { KIND_SPECS, kind_entry }
    project.kinds --> project.template_registry.TemplateRegistry.list_kinds { KIND_SPECS }
    project.kinds --> project.template_registry._core_template { kind_spec }
    project.kinds --> scale.plugin._resolve_deploy_target { resolve_entry }
    project.kinds --> scale.runtime.fleet._has_client { kind_has_client }
    project.kinds --> server.static_files { kind_has_client }
    project.mobui_scope --> compiler.passes.jsx_intrinsic_guard_pass { mobui_module_exempt }
    project.mobui_scope --> compiler.types.type_evaluator.TypeEvaluator._is_mobui_module { mobui_module_exempt }
    project.modresolver --> cli.commands.fix._verify_claims { find_jac_project_root }
    project.modresolver --> cli.commands.fix.fix { find_jac_project_root }
    project.modresolver --> client.compiler.ViteCompiler.compile_desktop_sdk { resolve_jac_virtual_module_exports, resolve_jac_virtual_module_path }
    project.modresolver --> compiler.tests.test_jac_mobui_typing { resolve_jac_virtual_module_path }
    project.modresolver --> dist.publish.py_imports { resolve_module }
    project.modresolver --> dist.publish.runtime_vendor._module_to_file { resolve_local_module }
    project.modresolver --> lsp.server.engine.JacLangServer._module_spec_target { resolve_client_npm_declarations, resolve_client_npm_package }
    project.modresolver --> lsp.server.engine.JacLangServer._npm_item_location { resolve_client_npm_declarations, resolve_client_npm_package }
    project.modresolver --> project.apps.resolve_entry_path { resolve_local_module }
    project.modresolver --> project.config.find_project_root { find_project_root as _find_project_root }
    project.modresolver --> project.workspace { find_jac_project_root }
    project.modresolver --> runtime.runtime { find_jac_project_root, infer_language, pop_import_base, push_import_base }
    project.modresolver --> server.outbox.outbox_db_path { find_jac_project_root }
    project.modresolver --> testing.cl_test_runner._compile_runtime { resolve_jac_virtual_module_path }
    project.placement --> cli.commands.fix._verify_claims { module_dot_path }
    project.placement --> project.kinds.resolve_app_kind { match_pin, validate_pins }
    project.plugin_config --> byllm.config_loader { PluginConfigBase }
    project.plugin_config --> client.config_loader { PluginConfigBase, deep_merge }
    project.plugin_config --> client.desktop_config { PluginConfigBase }
    project.plugin_config --> scale.config.config_loader { PluginConfigBase }
    project.providers --> cli.commands.execution._ensure_watchdog_installed { InstallContext, get_python_provider }
    project.providers --> cli.commands.execution._load_cwd_config { initialize_provider_registry }
    project.providers --> cli.commands.execution._serve_with { initialize_provider_registry }
    project.providers --> cli.commands.project.deps { resolve_plan }
    project.providers --> cli.commands.project.install { InstallContext, get_provider_registry, get_python_provider, resolve_plan }
    project.providers --> cli.commands.project.remove { InstallContext, get_python_provider }
    project.providers --> cli.commands.project.update { InstallContext, get_python_provider }
    type project.providers --> client.cli { EcosystemProvider }
    project.providers --> client.cli._npm_context { get_provider_registry }
    project.providers --> client.cli.run_npm_add { InstallContext }
    project.providers --> client.cli.run_npm_remove { InstallContext }
    project.providers --> client.npm_provider { EcosystemProvider, InstallContext, ResolvedDependency, manifest_plugin_deps }
    type project.providers --> client.plugin_config { EcosystemProvider }
    project.providers --> client.targets.react_native.scaffold { manifest_plugin_subdeps }
    project.providers --> dist.publish.package_json.npm_dependencies { manifest_plugin_deps }
    project.providers --> dist.seal.vendor_jab_deps { get_python_provider, resolve_plan }
    project.providers --> dist.source.project._requirements { get_python_provider, resolve_plan }
    project.providers --> scale.injector.bundle._resolved_python_specs { get_python_provider, resolve_plan }
    project.providers --> scale.injector.bundle._venv_stage { write_venv_deps_marker }
    project.providers --> scale.injector.bundle.staged_venv_files { VENV_DEPS_MARKER }
    project.providers --> scale.tests.microservices.test_fat_bundle { write_venv_deps_marker }
    project.providers --> scale.utils.vendor_wheels { get_python_provider, resolve_plan }
    project.pyvenv --> cli.commands.execution._discover_config_from_file { add_venv_to_path }
    project.pyvenv --> cli.commands.execution._ensure_watchdog_installed { add_venv_to_path }
    project.pyvenv --> cli.commands.execution._pin_run_scope { add_venv_to_path }
    project.pyvenv --> cli.commands.project.install { ensure_venv, get_venv_site_packages, make_git_spec }
    project.pyvenv --> cli.commands.project.update { make_git_spec }
    project.pyvenv --> cli.dispatch._discover_project_config { add_venv_to_path }
    project.pyvenv --> client.targets.desktop._dev_launch { get_venv_site_packages }
    project.pyvenv --> dist.jab_vendor._pip { pip_command, pip_env, pip_python }
    project.pyvenv --> project.capabilities.ensure_global_capability { pip_command, pip_env, pip_python }
    project.pyvenv --> project.providers { ensure_venv, get_venv_site_packages, make_git_spec, make_pip_spec, run_pip, summarize_pip_failure }
    project.pyvenv --> project.providers.PythonProvider._install_global { pip_command, pip_env, pip_python }
    project.pyvenv --> project.tool_paths { get_venv_site_packages }
    project.pyvenv --> scale.injector.bundle._venv_stage { get_venv_site_packages }
    project.pyvenv --> scale.injector.bundle.staged_venv_files { get_venv_site_packages }
    project.textio --> cli.commands.analysis._iter_jac_files { drop_git_ignored }
    project.source --> cli.commands.analysis._normalize_ignore_patterns { normalize_exclude_patterns }
    project.source --> cli.commands.analysis._should_ignore { path_matches_exclude }
    project.source --> client.client_diagnostics.ClientDiagnostic.render { render_diagnostic }
    project.source --> compiler.passes.context.Alert.as_log { render_diagnostic_header }
    project.source --> compiler.passes.context.Alert.pretty_print { render_diagnostic }
    project.source --> compiler.passes.import_wiring_pass { pascal_to_snake }
    project.source --> compiler.passes.pyast_load_pass.PyastBuildPass.convert { pascal_to_snake }
    project.source --> compiler.tools.jac_auto_lint_pass.JacAutoLintPass._is_file_excluded { path_matches_exclude }
    project.source --> compiler.tools.lang_tools { pascal_to_snake }
    project.source --> runtime.traceback_render { pretty_print_source_location }
    project.source --> scale.injector.bundle.BundleSourceFilter.matching_ignore_pattern { path_matches_exclude }
    project.source --> scale.injector.bundle.BundleSourceFilter.parks { path_matches_exclude }
    project.template_loader --> cli.commands.fix._ensure_workspace { migrate_implicit_app }
    project.template_loader --> cli.commands.project._create_app { scaffold_app }
    project.template_loader --> cli.commands.project._create_body { load_template_from_directory }
    project.template_loader --> cli.commands.project._resolve_bundled_template { load_template_from_directory }
    project.template_loader --> cli.commands.project._resolve_template { load_template_from_directory }
    project.template_loader --> cli.shadcn.cli._build_shadcn_template_info { load_template_from_directory }
    project.template_loader --> client.plugin_config._load_template { load_template_from_directory }
    type project.template_registry --> cli.commands.project { ProjectTemplate, TemplateRegistry }
    project.template_registry --> cli.commands.project._create_body { TemplateRegistry, get_template_registry }
    project.template_registry --> cli.mcp.compiler_bridge.CompilerBridge.list_templates._do_list_templates { get_template_registry }
    project.template_registry --> project.template_loader { ProjectTemplate, template_kind_for }
    project.tomlio --> cli.commands.config { read_toml_with_encoding }
    project.tomlio --> cli.commands.project._toml_apps_and_default { read_toml_with_encoding }
    project.tomlio --> cli.dispatch._discover_project_config { MalformedJacTomlError }
    project.tomlio --> project.config.JacConfig.load { read_toml_with_encoding }
    project.tomlio --> project.config.JacConfig.merge_from_toml_file { read_toml_with_encoding }
    project.tomlio --> project.config.JacConfig.save { MalformedJacTomlError }
    project.tomlio --> project.template_loader { read_toml_with_encoding }
    project.tool_paths --> cli.commands.execution._tool_site_dirs { python_global_site, python_project_site }
    project.tool_paths --> cli.commands.execution._tool_tiers { node_bin_dir, python_global_site, python_project_site }
    project.tool_paths --> client.cli.run_npm_add_global { node_root }
    project.workspace --> cli.commands.analysis.check { workspace_for_path }
    project.workspace --> cli.commands.fix._access_plan { workspace_for_path }
    project.workspace --> compiler.driver.application._warn_private_declarations { app_for_path }
    project.workspace --> dist.precompile_bytecode._application_sources { workspace_for_path }
    project.workspace --> lsp.server.engine.JacLangServer.type_check_file { workspace_for_path }
    project.workspace --> project.kinds.resolve_app_kind { workspace_for_path }
    project.textio --> cli.commands.architecture._arch_files { drop_git_ignored }
    project.app_kinds --> compiler.driver.pipeline_runner.compile_application { kind_has_client }
    project.app_kinds --> compiler.driver.program.JacProgram.stamp_app_facts { UI_MOBUI }
    project.app_kinds --> compiler.placement.placement.project_has_server | compiler.placement.placement_pins { kind_codespace }
    project.config --> project.compiler_host.ProjectHost.check_settings { get_config }
    project.config --> project.compiler_host.ProjectHost.declared_dependencies { get_config_for_path }
    project.config --> project.compiler_host.ProjectHost.project_facts { get_config_for_path }
    project.config --> project.compiler_host.ProjectHost.lint_settings { JacConfig, get_config_for_path, get_explicit_config }
    project.config --> project.compiler_host.ProjectHost.project_defaults { JacConfig, get_config }
    project.kernel_check --> cli.commands.analysis._check_file_job { kernel_check, reached_modules, report_parity }
    project.kernel_snapshot --> project.compiler_host.ProjectHost.native_analyze { record_kernel_session }
    project.kernel_snapshot --> project.kernel_check { kernel_analysis }
    project.modresolver --> project.compiler_host.ProjectHost.has_npm_package { has_client_npm_package }
    project.modresolver --> project.compiler_host.ProjectHost.in_typeshed_tree { in_typeshed_tree }
    project.modresolver --> project.compiler_host.ProjectHost.is_path_alias { is_path_alias_import }
    project.modresolver --> project.compiler_host.ProjectHost.is_untyped_third_party { is_untyped_third_party_module }
    project.modresolver --> project.compiler_host.ProjectHost.jac_virtual_module_path { resolve_jac_virtual_module_path }
    project.modresolver --> project.compiler_host.ProjectHost.npm_declarations { resolve_client_npm_declarations }
    project.modresolver --> project.compiler_host.ProjectHost.project_root { find_jac_project_root }
    project.modresolver --> project.compiler_host.ProjectHost.resolve_local_module { resolve_local_module }
    project.modresolver --> project.compiler_host.ProjectHost.resolve_module { resolve_module }
    project.modresolver --> project.compiler_host.ProjectHost.resolve_npm_package { resolve_client_npm_package }
    project.modresolver --> project.compiler_host.ProjectHost.sibling_declaration { sibling_declaration_file }
    project.source --> project.textio { JACIGNORE_FILENAME, normalize_exclude_patterns }
    project.textio --> cli.commands.analysis._check_file_job { read_file_with_encoding as _read_src }
    project.textio --> cli.commands.analysis._format_single_file_worker | cli.commands.architecture | cli.commands.transform.py2jac | compiler.driver.compiler | compiler.tools.lang_tools | project.compiler_host.ProjectHost.read_source | project.config.JacConfig.save | project.template_loader.scaffold_app | project.tomlio | runtime.traceback_render { read_file_with_encoding }
    project.textio --> compiler.driver.compiler.JacCompiler.get_bytecode { read_file_with_encoding }
    project.textio --> client.client_diagnostics.ClientDiagnostic.render { read_file_with_encoding, span_for_file }
    project.textio --> scale.injector.bundle.source_filter_for { read_jacignore_patterns }
    project.workspace --> project.compiler_host.ProjectHost.app_for_path { app_for_path }
    project.workspace --> project.compiler_host.ProjectHost.session { workspace_scope }
    project.workspace --> project.compiler_host.ProjectHost.workspace { workspace_for_path }
    project.workspace_model --> compiler.driver.boundary_classify | compiler.driver.compilation_context { AppSpec }
    project.workspace_model --> compiler.frontend.host | compiler.frontend.kernel_host | compiler.frontend.kernel_inputs | project.workspace { AppSpec, WorkspaceSpec }
    type project.workspace_model --> project.compiler_host { AppSpec, WorkspaceSpec }
    project.config --> cli.commands.execution._load_executable { get_config_for_path }
    project.config --> cli.commands.project._resolve_template { get_config }
    project.config --> cli.commands.project.publish { get_config }
    project.config --> packages.commands | packages.install | packages.provider | packages.publish | packages.resolve | packages.verify._verify_library { JacConfig }
    project.config --> packages.lock { toml_value }
    project.config --> packages.migrate { serialize_toml, toml_minimal_update }
    project.config --> project.package_scope.declared_package_name { get_config_for_dir }
    project.config --> project.package_scope.package_exports { get_config_for_dir }
    project.dependencies --> packages.commands | packages.resolve | project.config { PackageDep }
    project.dependencies --> packages.migrate { migrate_dependency_table }
    project.dependencies --> project.config.JacConfig.merge_dependency_tables { split_dependency_table }
    project.jac_version --> packages.resolve | packages.templates { satisfies as jac_satisfies }
    project.jac_version --> scale.injector.binary { exact_pin, is_plain_version, satisfies, split_clause, version_key }
    project.jac_version --> scale.tests.deploy.test_memory_trigger_guard { version_key }
    project.jac_version --> scale.tests.deploy.test_version_pin { exact_pin, version_key }
    project.modresolver --> dist.precompile_bytecode.image_mount_prefix { project_mounts }
    project.modresolver --> project.compiler_host.ProjectHost.project_facts { project_mounts_dir }
    project.modresolver --> project.compiler_host.package_name_of { is_scoped_package_name }
    project.modresolver --> project.package_scope { MOUNTS_DIR_NAME, is_scoped_package_name, module_name_in }
    project.modresolver --> project.package_scope.package_root_of { find_jac_project_root }
    project.package_scope --> compiler.driver.jir._module_cache_root { in_store }
    project.package_scope --> compiler.driver.jir._module_projection { is_dependency_module }
    project.package_scope --> dist.seal.vendor_packages | packages.mounts { mounts_dir }
    project.package_scope --> packages.artifact.project_role | packages.commands | packages.index | packages.install | packages.publish | packages.resolve | packages.templates | packages.verify | project.dependencies { is_package_name }
    project.package_scope --> packages.store { store_root }
    project.persistence --> project.config { PersistenceConfig }
    project.persistence --> project.config._parse_toml_data { parse_persistence }
    project.providers --> cli.commands.project._rewrite_compatible_pins { get_python_provider }
    project.providers --> cli.commands.project._update_pypi { get_python_provider }
    project.providers --> packages.commands { InstallContext, get_provider_registry, get_python_provider, resolve_plan }
    project.providers --> packages.provider { EcosystemProvider, InstallContext, ResolvedDependency }
    type project.providers --> cli.commands.project { InstallContext }
    project.pyvenv --> cli.commands.project._update_pypi { make_git_spec }
    project.pyvenv --> packages.commands._org_collisions { get_venv_site_packages }
    project.textio --> compiler.driver.nativecache._module_files_and_imports { read_file_with_encoding }
    project.workspace --> cli.commands.execution._load_executable | server.session.project_database { workspace_for_path }
    project.workspace --> project.persistence { persistence_namespace }
    project.config --> scale.deploy.target.kubernetes.manifest_builder { JacConfig, ServeConfig }
    project.kernel_check --> project.kernel_compile.kernel_compile_reported { alert_of }
    project.kernel_compile --> compiler.driver.application._kernel_units { forget_application_units, kernel_compile_application }
    project.kernel_compile --> compiler.driver.application._prepare { host_prepared }
    project.kernel_compile --> compiler.driver.application._prepare_revision { host_preparing }
    project.kernel_compile --> project.compiler_host.ProjectHost.kernel_compile { host_kernel_compile }
    project.kernel_snapshot --> project.compiler_host.ProjectHost.kernel_inputs { session_inputs }
    project.kernel_snapshot --> project.kernel_check { host_deferred }
    project.kernel_snapshot --> project.kernel_compile { COMPILE_ENTRY, KernelAnalysisError, _IFACE_BUILT, call_with_asker, host_deferred, kernel_snapshot, loaded_kernel, other_compiler_report }
    project.modresolver --> project.kernel_snapshot.other_compiler_dir { COMPILER_PACKAGE }
    project.modresolver --> project.kernel_snapshot.session_inputs { get_jac_search_paths, get_typeshed_paths }
    project.client_paths --> compiler.driver.application._prepare_revision { client_input_dirs }
    project.config --> artifacts.router._provision { offline_mode }
    type project.config --> data.pg_dist | server.session { DatabaseConfig }
    project.config --> data.pg_dist._configured_dist { get_config }
    project.config --> data.pg_dist._database_config { get_config }
    project.config --> project.kernel_snapshot.catalog_build_blocker { offline_mode }
    project.config --> scale.config.dev_config.local_pod_binary { get_config_for_path }
    project.config --> server.session._database_config { DatabaseConfig, get_config_for_dir }
    project.config --> toolchains.host.use_system_tools { use_system_toolchains }
    project.config --> toolchains.store.offline { offline_mode }
    project.kernel_compile --> compiler.driver.application._release_compile_state { forget_application_units }
    project.kernel_compile --> compiler.driver.compiler.JacCompiler.kernel_native_entry { kernel_generates_native }
    project.kernel_snapshot --> compiler.driver.application._release_compile_state { forget_interface_memo }
    project.modresolver --> compiler.backends.py.artifact_imports.resolve_imports { project_mounts }
    project.providers --> packages.commands { venv_deps_satisfied }
    runtime.archetype --> byllm.llm._mock_jsonable { Archetype }
    runtime.archetype --> byllm.visit_routing { Anchor, Archetype, ObjectSpatialFunction }
    runtime.archetype --> byllm.visit_routing._candidate_for { EdgeAnchor, EdgeArchetype, NodeAnchor, NodeArchetype }
    runtime.archetype --> byllm.visit_routing._route_context { EdgeAnchor, EdgeArchetype, NodeAnchor, NodeArchetype, WalkerAnchor }
    runtime.archetype --> compiler.native_compiler.NativeCompiler._register { NodeAnchor, NodeArchetype }
    runtime.archetype --> data.query_planner { Anchor, EdgeAnchor, anchor_key }
    runtime.archetype --> data.query_planner._acl_pushdown_root { Archetype, Root }
    runtime.archetype --> data.serializer { Access, AccessLevel, Anchor, EdgeAnchor, NodeAnchor, ObjectAnchor, Permission, WalkerAnchor, access_level_cast }
    runtime.archetype --> lib.jaclib { GenericEdge, ObjectSpatialFunction as DSFunc, Root }
    runtime.archetype --> runtime.constructs { AccessLevel, Anchor, Archetype, EdgeAnchor, EdgeArchetype, GenericEdge, JsxElement, NodeAnchor, NodeArchetype, ObjectSpatialFunction, PermissionDenied, Root, WalkerAnchor, WalkerArchetype, access_level_cast }
    runtime.archetype --> runtime.context { NodeAnchor, PermissionDenied, Root }
    runtime.archetype --> runtime.graph_query { Anchor, anchor_key }
    runtime.archetype --> runtime.graph_utils.collect_node_connections { EdgeAnchor, NodeAnchor, anchor_key }
    runtime.archetype --> runtime.graph_utils.traverse_graph { EdgeAnchor }
    runtime.archetype --> runtime.graph_walk { Anchor, EdgeAnchor, NodeAnchor, anchor_key, light_edge_view, same_anchor }
    runtime.archetype --> runtime.graph_walk.acl_read_ok { AccessLevel }
    runtime.archetype --> runtime.memory { Anchor, Root }
    runtime.archetype --> runtime.osp_graph_sv { Anchor, EdgeAnchor, NodeAnchor, anchor_key, same_anchor }
    runtime.archetype --> runtime.osp_kernel_sv { EdgeAnchor, NodeAnchor, ObjectSpatialFunction, WalkerArchetype }
    runtime.archetype --> runtime.runtime { GenericEdge, ObjectAnchor, ObjectSpatialFunction, Root, _deref, _edge_subtypes, _light_edge_types, anchor_key, edge_subtypes, is_light_edge_type, light_clear_hop, light_connect, light_disconnect, light_edge_view, light_hop, light_hop_answers, same_anchor }
    runtime.archetype --> runtime.runtime.JacLLM.by_operator { EdgeArchetype, NodeArchetype }
    runtime.archetype --> server.session { Anchor, EdgeAnchor, NodeAnchor, Root }
    runtime.build_services --> client.runtime_source.client_runtime_cl_basename { build_services }
    runtime.build_services --> compiler.driver.build_services { BuildServices }
    runtime.build_services --> runtime.runtime.JacRuntime.get_compiler { build_services }
    runtime.build_services --> runtime.runtime.JacRuntime.get_program { build_services }
    runtime.build_services --> runtime.runtime.JacRuntime.get_selfhost { build_services }
    runtime.build_services --> runtime.runtime.JacServe.get_client_bundle_builder { build_services }
    runtime.build_services --> runtime.runtime.JacTest.run_test { build_services }
    runtime.build_services --> scale.runtime.fleet._compiled_app_edges { build_services }
    runtime.build_services --> testing.testing.JacTestClient._ensure_initialized { build_services }
    runtime.build_services --> testing.testing.JacTestClient.reload { build_services }
    runtime.builtin --> cli.commands.tools.dot { printgraph }
    runtime.builtin --> runtime.archetype.Archetype.__init_subclass__ { _jac_region_instrument }
    runtime.builtin --> scale.server.jobs_ext { ScheduleTrigger }
    runtime.builtin --> scale.server.webhook_ext { APIProtocol }
    runtime.builtin --> scale.server.websocket_ext { APIProtocol }
    runtime.builtin as blt --> scale.tests.server.test_restspec;
    runtime.builtin --> scale.tests.server.test_restspec { APIProtocol }
    runtime.builtin --> scale.tests.server.test_webhook { APIProtocol, restspec }
    runtime.builtin --> server.endpoints.walkers { APIProtocol }
    runtime.builtin --> server.server { APIProtocol }
    runtime.builtin --> server.server.JacAPIServer._register_scheduled_tasks { ScheduleTrigger }
    runtime.builtin --> server.task_scheduler { ScheduleTrigger }
    runtime.cinterop as _cinterop_mod --> runtime.builtin.__getattr__;
    runtime.constants --> compiler.backends.py.jcir_gen_pass { Constants as Con, EdgeDir }
    runtime.constants --> compiler.frontend.parser.parser { EdgeDir }
    runtime.constants --> compiler.frontend.unitree { Constants as Con, EdgeDir }
    runtime.constants --> compiler.passes.graph_lowering_pass { EdgeDir }
    runtime.constants --> compiler.tools.normalize_pass { EdgeDir }
    runtime.constants --> compiler.types.type_evaluator { EdgeDir }
    runtime.constants --> data.dbcatalog.holds_no_data { Constants as Con }
    runtime.constants --> lib.jaclib { EdgeDir }
    runtime.constants --> runtime.archetype { EdgeDir }
    runtime.constants --> runtime.context { Constants as Con }
    runtime.constants --> runtime.runtime { EdgeDir, colors }
    runtime.constants --> scale.admin.admin_portal { Constants as Con }
    runtime.constants --> scale.server.inprocess { Constants as Con }
    runtime.constants --> scale.server.websocket_ext { Constants as Con }
    runtime.constants --> scale.tests.data.test_eager_spawn { Constants as Con }
    runtime.constants --> scale.tests.microservices.test_microservice { Constants as Con }
    runtime.constants --> server.endpoints.colocated { Constants as Con }
    runtime.constants --> server.endpoints.pages { Constants as Con }
    runtime.constants --> server.endpoints.walkers { Constants as Con }
    runtime.constants --> server.identity.identity_storage { Constants as Con }
    runtime.constants --> server.identity.user_manager { Constants as Con }
    runtime.constants --> server.server { Constants as Con }
    runtime.constructs --> cli.commands.execution._invoke_entrypoint { WalkerArchetype }
    runtime.constructs --> data.serializer { Archetype, GenericEdge, NodeArchetype, Root, WalkerArchetype }
    runtime.constructs --> lib.jaclib { Archetype as Obj, EdgeArchetype as Edge, JsxElement, NodeArchetype as Node, WalkerArchetype as Walker }
    type runtime.constructs --> runtime.builtin { AccessLevel, NodeArchetype }
    runtime.constructs --> runtime.builtin._get_access_level { AccessLevel }
    type runtime.constructs --> runtime.graph_utils { EdgeArchetype, NodeArchetype }
    runtime.constructs --> runtime.runtime { AccessLevel, Anchor, Archetype, EdgeAnchor, EdgeArchetype, JsxElement, NodeAnchor, NodeArchetype, PermissionDenied, WalkerAnchor, WalkerArchetype, access_level_cast }
    runtime.constructs --> scale.memory.context.JScaleExecutionContext.init { PermissionDenied }
    runtime.constructs --> server.identity.identity_storage.IdentityStorage.create_user { Root }
    runtime.constructs --> server.identity.identity_storage.IdentityStorage.ensure_user_by_id { Root }
    runtime.constructs --> server.identity.identity_storage.IdentityStorage.reset_root { Root }
    type runtime.constructs --> server.server { Archetype, WalkerArchetype }
    runtime.constructs --> server.server.ExecutionManager.spawn_walker_async { NodeArchetype }
    runtime.constructs --> server.server.ExecutionManager.spawn_walker_sync { NodeArchetype }
    runtime.constructs --> server.server.ModuleIntrospector.scheduled_members { WalkerArchetype }
    runtime.constructs --> server.session._ancestry_of { Archetype, EdgeArchetype, NodeArchetype, WalkerArchetype }
    runtime.constructs --> server.task_scheduler.Scheduler._execute { WalkerArchetype }
    type runtime.context --> cli.commands.cli_helpers { ExecutionContext }
    type runtime.context --> runtime.runtime { ExecutionContext }
    runtime.context --> runtime.runtime.JacContext.create_j_context { ExecutionContext }
    runtime.context --> scale.memory.context { CallState, ExecutionContext }
    runtime.context --> scale.plugin { ExecutionContext }
    type runtime.context --> scale.runtime.provider { ExecutionContext }
    type runtime.context --> scale.server.inprocess { ExecutionContext }
    runtime.context --> scale.tests.server.test_middleware_async_root { ExecutionContext }
    runtime.context --> server.server { CallState, ExecutionContext }
    runtime.context --> server.sv_client._local_spawn { ExecutionContext }
    runtime.debugger --> cli.commands.execution.debug { debugger as db }
    runtime.exceptions --> data.store { WriteConflict }
    runtime.exceptions --> runtime.context { MissingAnchorError }
    runtime.exceptions --> server.middleware { MissingAnchorError }
    runtime.exceptions --> server.server { ReadOnlyRetry, WriteConflict }
    runtime.exceptions --> server.server._abegin_user_request_context { MissingAnchorError }
    runtime.exceptions --> server.session { ReadOnlyRetry, WriteConflict }
    runtime.graph_query --> data.query_planner { GraphQuery, QPred }
    runtime.graph_query --> data.sqlcompile { GraphQuery, QHop, QPred }
    runtime.graph_query --> lib.jaclib { GraphQuery, QHop, QOrder, QPred }
    runtime.graph_query --> runtime.graph_walk { GraphQuery, QHop, QPred }
    runtime.graph_query --> runtime.runtime { GraphQuery, QHop, QPred, filter_query_nodes }
    runtime.graph_utils --> runtime.builtin._jac_graph_json { collect_node_connections }
    runtime.graph_utils --> runtime.runtime.JacBuiltin.printgraph { traverse_graph }
    runtime.graph_utils --> scale.admin.admin_portal.JacAPIServerAdmin.admin_graph_data { collect_node_connections }
    runtime.graph_utils --> scale.injector.binary { host_arch, host_os, release_arch }
    runtime.graph_utils --> scale.injector.binary_injector { host_arch }
    runtime.graph_utils --> scale.tests.microservices.test_binary_injector { host_arch }
    runtime.graph_utils --> scale.utils.vendor_wheels { release_arch }
    runtime.graph_utils --> server.endpoints.pages.register_graph_endpoints.graph_data { collect_node_connections }
    runtime.graph_utils --> server.session.project_db_name { get_name }
    runtime.graph_walk --> data.query_planner { access_gated, acl_read_ok, needs_store, origin_anchors, pred_subject, walk, walk_edges, walk_nodes }
    runtime.graph_walk --> runtime.runtime.JacGraph.refs { access_gated, has_persistent_origin, needs_store, origin_anchors, walk_edges, walk_nodes }
    runtime.interop_bridge --> compiler.backends.native.na_compile_pass.NativeCompilePass._run_impl { register_py_callbacks }
    runtime.interop_bridge --> compiler.driver.compiler.JacCompiler._load_native_from_cache { register_py_callbacks }
    runtime.interop_bridge --> runtime.prepared.execute_module { NativeLibrary }
    runtime.interop_bridge --> runtime.source_app._load_application { NativeCallback, NativeLibrary }
    runtime.memory --> runtime.context | server.session { Memory }
    type runtime.native_library --> cli.commands.execution { SharedNativeEngine }
    type runtime.native_library --> compiler.driver.compiler { SharedNativeEngine }
    runtime.native_library --> compiler.driver.compiler.JacCompiler._load_native_from_cache { SharedNativeEngine }
    runtime.native_library --> compiler.driver.compiler.JacCompiler._sealed_native_engine { shared_engine_for }
    type runtime.native_library --> compiler.frontend.codeinfo { SharedNativeEngine }
    runtime.object_interop --> byllm.llm._mock_jsonable { fields, is_record }
    runtime.object_interop --> byllm.schema { is_record }
    runtime.object_interop --> byllm.tests.test_mtir_integration { fields }
    runtime.object_interop --> byllm.visit_routing { fields, is_record }
    runtime.object_interop --> cli.NonGPT { fields as dc_fields, is_record }
    runtime.object_interop --> compiler.native_compiler.NativeCompiler._field_annotations { fields }
    runtime.object_interop --> compiler.native_compiler.NativeCompiler._register_defaults { fields }
    runtime.object_interop --> comptime { fields as _record_fields, is_record as _is_record }
    runtime.object_interop --> data.contracts { fields, is_record }
    runtime.object_interop --> data.schema_rules { fields, is_record }
    runtime.object_interop --> data.serializer { fields, is_record }
    runtime.object_interop --> runtime.typecache { fields, is_record }
    runtime.object_interop --> server.server { fields as record_fields, is_record }
    runtime.object_interop --> server.serving.coerce { is_record }
    runtime.object_interop --> server.serving.model { fields, is_record }
    runtime.object_model --> cli.NonGPT { MISSING }
    runtime.object_model --> compiler.native_compiler.NativeCompiler._field_annotations { MISSING }
    runtime.object_model --> compiler.native_compiler.NativeCompiler._register_defaults { MISSING }
    runtime.object_model --> comptime { MISSING as _MISSING, ObjectField as _field }
    runtime.object_model --> data.contracts { MISSING }
    runtime.object_model --> data.serializer { MISSING }
    runtime.object_model --> runtime.archetype { ObjectField, asdict, fields, is_jac_object, make_object }
    runtime.object_model --> runtime.context { MISSING }
    runtime.object_model --> runtime.object_interop { MISSING, ObjectField, fields as jac_fields, is_jac_object }
    runtime.object_model --> runtime.object_pydantic { MISSING, fields }
    runtime.object_model --> runtime.runtime { make_object }
    runtime.object_model --> scale.memory.context { MISSING }
    runtime.object_model --> scale.sdk.spec.DeploySpec.from_config { fields }
    runtime.object_model --> scale.server.sso_ext { asdict }
    runtime.object_model --> server.server { MISSING }
    runtime.object_pydantic --> runtime.object_model._pydantic_schema { object_schema }
    runtime.osp_graph as _graph --> runtime.osp_graph_sv;
    runtime.osp_graph_sv --> byllm.visit_routing._candidate_for { sv_register_hydrated }
    runtime.osp_graph_sv --> runtime.archetype.EdgeAnchor.detach { sv_forget_edge }
    runtime.osp_graph_sv --> runtime.graph_utils.collect_node_connections { sv_live_edges, sv_register_hydrated }
    runtime.osp_graph_sv --> runtime.graph_utils.traverse_graph { sv_register_hydrated }
    runtime.osp_graph_sv --> runtime.osp_kernel_sv { cls_of_tag, tag_of_cls }
    runtime.osp_graph_sv --> runtime.runtime.JacAccessValidation._groups_of { sv_live_edges, sv_register_hydrated }
    runtime.osp_graph_sv --> runtime.runtime.JacContext.reset_graph { sv_forget_by_id }
    runtime.osp_graph_sv --> runtime.runtime.JacGraph.disconnect { sv_candidate_edges_between, sv_register_hydrated }
    runtime.osp_graph_sv --> runtime.runtime.JacGraph.heavy_edge { sv_conn }
    runtime.osp_graph_sv --> server.session.Session._drop_snapshot_reads { sv_forget_edge }
    runtime.osp_graph_sv --> server.session.Session.close { sv_store_closed }
    runtime.osp_graph_sv --> server.session.Session.quarantine_ref { sv_forget_by_id }
    runtime.osp_kernel --> byllm.visit_routing._route_context { _current_scope }
    runtime.osp_kernel --> compiler.backends.es.esast_gen_pass { osp_skip_rest }
    runtime.osp_kernel --> compiler.backends.py.jcir_gen_pass { osp_skip_rest }
    runtime.osp_kernel --> compiler.passes.comptime_resolve_pass { osp_skip_rest }
    runtime.osp_kernel --> compiler.passes.context.CompileContext.enter_node { osp_skip_rest }
    runtime.osp_kernel --> compiler.passes.context.CompileContext.exit_node { osp_skip_rest }
    runtime.osp_kernel --> compiler.passes.jsx_intrinsic_guard_pass { osp_skip_rest }
    runtime.osp_kernel --> compiler.passes.scope_walk { osp_skip_rest }
    runtime.osp_kernel --> compiler.tools.grammar_extract_pass { osp_skip_rest }
    runtime.osp_kernel as _kernel --> runtime.osp_kernel_sv;
    runtime.osp_kernel --> runtime.osp_kernel_sv { OspNodeDesc, OspRuntime, OspSlot, OspWalkScope, OspWalkerDesc, UNTYPED }
    runtime.osp_kernel --> runtime.runtime.JacBuiltin.log_report { _current_scope, osp_report }
    runtime.osp_kernel --> runtime.runtime.JacGraph.clear_edges { osp_forget }
    runtime.osp_kernel --> runtime.runtime.JacPersistence.destroy { osp_forget }
    runtime.osp_kernel --> runtime.runtime.JacWalker.disengage { osp_disengage }
    runtime.osp_kernel --> runtime.runtime.JacWalker.spawn_call { osp_spawn }
    runtime.osp_kernel --> runtime.runtime.JacWalker.visit { osp_visit, scope_of }
    runtime.osp_kernel_sv --> runtime.runtime.JacWalker.async_spawn_call { desc_for, make_sv_runtime, osp_spawn_async }
    runtime.osp_kernel_sv --> runtime.runtime.JacWalker.spawn_call { desc_for, make_sv_runtime }
    runtime.osp_kernel_sv --> server.server._begin_request_context { isolate_request_walk_stack }
    runtime.osp_tag --> compiler.backends.es.esast_gen_pass.EsastGenPass._build_osp_tags_js { stable_osp_tag }
    runtime.osp_tag --> compiler.backends.es.esast_gen_pass.EsastGenPass._edge_tag_literal { stable_osp_tag }
    runtime.osp_tag --> compiler.backends.es.esast_gen_pass.EsastGenPass._osp_slots_js { stable_osp_tag }
    runtime.osp_tag --> compiler.backends.native.na_ir_gen_pass { stable_osp_tag }
    runtime.osp_tag --> compiler.backends.py.jcir_gen_pass.JcirGenPass.exit_module { stable_osp_tag }
    runtime.osp_tag --> compiler.jc_unit._alert_tag { stable_osp_tag }
    runtime.osp_tag --> compiler.native_compiler { stable_osp_tag }
    runtime.osp_tag --> compiler.passes.osp_analysis { stable_osp_tag }
    runtime.osp_tag --> runtime.osp_graph_sv.tag_of_cls { stable_osp_tag }
    runtime.portability --> compiler.placement.placement_solver._py_import_client_portable { supports }
    runtime.prepared --> cli.commands.execution.serve { initialize_application }
    runtime.prepared --> client.targets.client_dev_common.dev_proxy_paths { prepared_manifest }
    type runtime.prepared --> compiler.driver.application { PreparedApplication }
    runtime.prepared --> compiler.driver.application._prepare { PreparedApplication, publish }
    runtime.prepared --> compiler.driver.application._prepare_sealed { PreparedApplication, publish }
    runtime.prepared --> compiler.driver.application.prepare_application { publish }
    runtime.prepared --> compiler.driver.application.prepare_dynamic_module { publish }
    type runtime.prepared --> compiler.driver.build_services { PreparedApplication }
    runtime.prepared --> dist.source.client { PreparedApplication }
    runtime.prepared --> dist.source.project { PreparedApplication, application_namespace }
    runtime.prepared --> project.config.JacConfig.app_for_path { origin_for_source }
    type runtime.prepared --> runtime.build_services { PreparedApplication }
    type runtime.prepared --> runtime.prepared_loader { PreparedApplication }
    runtime.prepared --> runtime.prepared_loader.PreparedFinder.find_spec { _applications, application_namespace, entry_alias }
    runtime.prepared --> runtime.prepared_loader.PreparedLoader.exec_module { execute_module }
    runtime.prepared --> runtime.runtime.JacLLM.get_mtir_from_map { semantic_for_scope }
    runtime.prepared --> runtime.runtime.JacModule.impl_patch_filename.decorator { application_for }
    runtime.prepared --> runtime.source_app { PreparedApplication, initialize_application, publish }
    runtime.prepared --> scale.server.inprocess.prepare_inprocess_runtime { initialize_application }
    type runtime.prepared --> server.assembly { PreparedApplication }
    runtime.prepared --> server.assembly.colocate_services { load_prepared_module }
    runtime.prepared --> server.endpoint_contract.check_endpoint_contract { application_for }
    runtime.prepared --> server.hmr.HotReloader._dispatch_change { application_for }
    runtime.prepared --> server.hmr.HotReloader._reload_server_module { application_for, initialize_application }
    runtime.prepared --> server.sealed_serve.client_dist_for { application_for }
    runtime.prepared --> server.sealed_serve.serve_manifest_for { prepared_manifest }
    runtime.prepared --> server.server.JacAPIServer._ensure_client_bundle { application_for }
    runtime.prepared --> server.server.ModuleIntrospector._resolve_declared { application_for, load_prepared_module, source_for_origin }
    runtime.prepared --> testing.testing.JacTestClient._ensure_initialized { initialize_application }
    runtime.prepared --> testing.testing.JacTestClient.close { forget }
    runtime.prepared_loader --> runtime.prepared.ensure_namespace { PreparedLoader }
    runtime.prepared_loader --> runtime.prepared.publish { PreparedFinder }
    runtime.region --> runtime.archetype.Archetype.__init_subclass__ { is_drop_hook }
    runtime.region as _region_mod --> runtime.builtin.__getattr__;
    runtime.region --> runtime.runtime.JacPersistence.destroy { run_drop }
    runtime.runtime --> byllm.lib { JacRuntime }
    runtime.runtime --> byllm.tests.support.need_outside_jaclang { JacRuntime }
    runtime.runtime --> byllm.tests.test_byllm { JacRuntime }
    runtime.runtime --> byllm.tests.test_routing { JacRuntime }
    runtime.runtime --> byllm.visit_routing._candidate_for { JacRuntimeInterface }
    runtime.runtime --> byllm.visit_routing.route_visit { JacRuntime as Jac }
    runtime.runtime --> cli.commands.analysis.check.run_units { JacRuntime }
    runtime.runtime --> cli.commands.cli_helpers.proc_file { JacRuntime as Jac }
    runtime.runtime --> cli.commands.execution._discover_config_from_file { JacRuntime as Jac }
    runtime.runtime --> cli.commands.execution._exec_file { JacRuntime as Jac }
    runtime.runtime --> cli.commands.execution._invoke_entrypoint { JacRuntime as Jac }
    runtime.runtime --> cli.commands.execution._pin_run_scope { JacRuntime as Jac }
    runtime.runtime --> cli.commands.execution.serve { JacRuntime as Jac }
    runtime.runtime --> cli.commands.tools.dot { JacRuntime as Jac }
    runtime.runtime --> cli.console._get_console { JacRuntime as Jac }
    runtime.runtime --> cli.mcp.compiler_bridge.CompilerBridge.format_snippet._do_format { JacRuntime as Jac }
    runtime.runtime --> cli.mcp.compiler_bridge.CompilerBridge.get_ast_snippet._do_ast { JacRuntime as Jac }
    runtime.runtime --> cli.mcp.compiler_bridge.CompilerBridge.jac_to_js._do_jac2js { JacRuntime as Jac }
    runtime.runtime --> cli.mcp.compiler_bridge.CompilerBridge.jac_to_py._do_jac2py { JacRuntime as Jac }
    runtime.runtime --> cli.mcp.compiler_bridge.CompilerBridge.lint_snippet._do_lint { JacRuntime as Jac }
    runtime.runtime --> cli.mcp.compiler_bridge.CompilerBridge.parse_snippet._do_parse { JacRuntime as Jac }
    runtime.runtime --> cli.mcp.compiler_bridge.CompilerBridge.py_to_jac._do_py2jac { JacRuntime as Jac }
    runtime.runtime --> cli.mcp.compiler_bridge.CompilerBridge.typecheck_snippet._do_typecheck { JacRuntime as Jac }
    runtime.runtime --> client.cli.run_client_build { JacRuntime as Jac }
    runtime.runtime --> client.cli.run_client_setup { JacRuntime as Jac }
    runtime.runtime --> client.cli.run_client_start { JacRuntime as Jac }
    runtime.runtime --> client.client_bundle.client_program { JacRuntime }
    runtime.runtime --> client.route_scanner.resolve_route_exports { JacRuntime as Jac }
    runtime.runtime --> client.targets.client_dev_common.dev_proxy_paths { JacRuntime as Jac }
    runtime.runtime --> client.targets.mobile_target { JacRuntime as Jac }
    runtime.runtime --> client.targets.web_target.WebTarget.build { JacRuntime as Jac }
    runtime.runtime --> client.targets.web_target._get_client_function_name { JacRuntime as Jac }
    runtime.runtime --> client.vite_client_bundle.make_client_bundle_builder { JacRuntime as Jac }
    runtime.runtime --> compiler.driver.compiler.JacCompiler.selfhost.getter { JacRuntime }
    runtime.runtime --> compiler.driver.selfhost.SelfHostCache.program.getter { JacRuntime }
    runtime.runtime --> compiler.tests.test_stubcat_roundtrip.small_catalog { JacRuntime }
    runtime.runtime --> data.query_planner.LazyRefs._mem { JacRuntimeInterface }
    runtime.runtime --> data.query_planner._acl_pushdown_root { JacRuntimeInterface }
    runtime.runtime --> dist.seal.bake_serve_payloads { JacRuntime as Jac }
    runtime.runtime --> dist.seal.build_serve_manifest { JacRuntime as Jac }
    runtime.runtime --> lib.jaclib { JacRuntimeInterface }
    runtime.runtime --> project.config.JacConfig.app_for_target { JacRuntime }
    runtime.runtime --> project.plugin_config { JacRuntime }
    runtime.runtime --> runtime.archetype.EdgeAnchor.detach { JacRuntime }
    runtime.runtime --> runtime.archetype.NodeAnchor.all_edges { JacRuntimeInterface }
    runtime.runtime --> runtime.archetype.Root.__getattr__ { JacRuntime }
    runtime.runtime --> runtime.archetype._dirty_setattr { JacRuntime }
    type runtime.runtime --> runtime.builtin { LLMModel }
    runtime.runtime --> runtime.context.ExecutionContext.__post_init__ { JacRuntime }
    runtime.runtime --> runtime.graph_utils.collect_node_connections { resolve_ref }
    runtime.runtime --> runtime.graph_utils.get_name { JacRuntime }
    runtime.runtime --> runtime.graph_utils.traverse_graph { JacRuntimeInterface }
    runtime.runtime --> runtime.graph_walk.access_gated { JacRuntimeInterface }
    runtime.runtime --> runtime.graph_walk.acl_read_ok { JacRuntimeInterface }
    runtime.runtime --> runtime.interop_bridge._pyb_import_module { JacModule }
    runtime.runtime --> runtime.osp_graph_sv._mem_or_ctx { JacRuntime }
    runtime.runtime --> runtime.osp_kernel_sv._sv_on_complete { JacRuntime }
    runtime.runtime --> runtime.prepared.execute_module { JacRuntime as Jac }
    runtime.runtime --> runtime.prepared.load_prepared_module { JacRuntime as Jac }
    runtime.runtime --> runtime.source_app.main { JacRuntime as Jac }
    runtime.runtime --> scale.admin.admin_portal { JacRuntime as Jac }
    runtime.runtime --> scale.memory.context.JScaleExecutionContext.init { JacRuntime }
    runtime.runtime --> server.endpoints.pages { JacRuntime as Jac }
    runtime.runtime --> server.hmr.HotReloader._recompile_client_code { JacRuntime as Jac }
    runtime.runtime --> server.hmr.HotReloader._recompile_client_unified { JacRuntime as Jac }
    runtime.runtime --> server.hmr.HotReloader._reload_server_module { JacRuntime as Jac }
    runtime.runtime --> server.server.ModuleIntrospector._check_module_freshness { JacRuntime as Jac }
    runtime.runtime --> server.server.ModuleIntrospector._resolve_declared { JacRuntime as Jac }
    runtime.runtime --> server.serving.supervisor.WorkerSupervisor._spawn { JacRuntime }
    runtime.runtime --> server.shared_store.shared_store { JacRuntime }
    runtime.runtime --> server.static_files { JacRuntime as Jac }
    runtime.runtime --> server.sv_client._scale_transport { _scale_provider }
    runtime.runtime --> testing.runner { JacRuntimeInterface }
    runtime.runtime --> testing.test_runner._fresh_jac_state { JacRuntime, JacRuntimeInterface }
    runtime.scalars --> compiler.backends.es.esast_gen_pass.EsastGenPass._apply_fw_coercion { shape_of }
    runtime.scalars --> compiler.backends.es.esast_gen_pass.EsastGenPass._exit_name_impl { is_sized }
    runtime.scalars --> compiler.backends.es.esast_gen_pass.EsastGenPass._fw_binary { shape_of }
    runtime.scalars --> compiler.backends.es.jac_runtime_js._build_fw_runtime_js { numeric_shapes, range_of }
    runtime.scalars --> compiler.backends.es.jac_runtime_js._build_types_runtime_js { numeric_shapes }
    runtime.scalars --> compiler.backends.es.primitives_es.ESBuiltinEmitter.emit_abs { is_sized }
    runtime.scalars --> compiler.backends.es.primitives_es.ESBuiltinEmitter.emit_print { shape_of }
    runtime.scalars --> compiler.backends.es.primitives_es.ESBuiltinEmitter.emit_wrapping { is_sized }
    runtime.scalars --> compiler.backends.native.na_ir_gen_pass { ScalarShape, range_of, shape_of, wrap_value }
    runtime.scalars --> compiler.backends.py.jcir_facts { sized_scalar_names }
    runtime.scalars --> compiler.backends.py.jcir_gen_pass { shape_of }
    runtime.scalars --> compiler.passes.wasm_contract.value_contract { ScalarShape, shape_range }
    runtime.scalars --> compiler.type_registry { ScalarShape, numeric_shapes, shape_literal_fits, shape_range, shapes_unify, shapes_widen_to, sized_scalar_names }
    runtime.scalars --> compiler.types.ct_eval { shape_of }
    runtime.scalars --> compiler.types.fixed_width.adopt_literal { float_max }
    runtime.scalars --> comptime._scalar_size_align { shape_of }
    runtime.scalars --> runtime.builtin._is_sized_type_name { is_sized }
    runtime.scalars --> runtime.cinterop { numeric_shapes }
    runtime.scalars --> runtime.sized { numeric_shapes, range_of, shape_of, wrap_value }
    runtime.semantic --> byllm.mtir { FunctionInfo, Info, MethodInfo }
    runtime.semantic --> byllm.schema { ClassInfo, EnumInfo, FieldInfo, FunctionInfo, Info, ParamInfo, VarInfo }
    runtime.semantic --> byllm.tests.test_mtir_integration { ClassInfo, EnumInfo, FieldInfo, FunctionInfo, MethodInfo, ParamInfo, mk_dict, mk_list }
    runtime.semantic --> byllm.types | runtime.runtime { Info }
    runtime.semantic --> byllm.visit_routing { ClassInfo }
    type runtime.semantic --> compiler.driver.program { Info }
    type runtime.semantic --> compiler.driver.progstate { Info }
    runtime.semantic --> compiler.passes.mtir_gen_pass { ClassInfo, EnumInfo, FieldInfo, FunctionInfo, MethodInfo, ParamInfo, mk_dict, mk_list, type_to_str }
    type runtime.semantic --> runtime.prepared { Info }
    runtime.sized --> compiler.tests.test_fixed_width_equivalence { SIZED_TYPES }
    runtime.sized --> data.serializer.Serializer._declared_of { SIZED_TYPES }
    runtime.sized --> data.serializer.Serializer._serialize_value { json_wire_form }
    runtime.sized --> data.serializer.Serializer.coerce { json_wire_read }
    runtime.sized as _sized_mod --> runtime.builtin.__getattr__;
    runtime.source_app --> dist.source.project.export_project { SOURCE_FORMAT }
    runtime.surface --> compiler.frontend.codeinfo { SurfaceEntry }
    runtime.surface --> compiler.passes.boundary_analysis_pass.BoundaryAnalysisPass._record_surface { SurfaceEntry }
    runtime.surface --> server.server.ModuleIntrospector._load_surface { SurfaceEntry }
    runtime.traceback_render --> cli.commands.execution._exec_file { dump_traceback }
    runtime.traceback_render --> cli.commands.execution.serve { dump_traceback }
    runtime.typecache --> data.serializer { get_field_types }
    runtime.typecache --> data.serializer.Serializer.register { invalidate as _invalidate_typecache, warm as _warm_typecache }
    runtime.archetype --> runtime.graph_utils.collect_node_connections { AccessLevel }
    runtime.runtime --> runtime.graph_utils.collect_node_connections { JacRuntimeInterface }
    runtime.graph_utils --> compiler.backends.native.static_link.load_outline_atomics { triple_arch }
    runtime.portability --> compiler.placement.placement_solver { supports }
    runtime.semantic --> byllm.schema { TypeForm }
    runtime.semantic --> byllm.tests.test_mtir_integration { TypeForm, mk_form, type_to_str }
    runtime.semantic --> compiler.passes.mtir_gen_pass { TypeForm, mk_form }
    runtime.build_services --> runtime.prepared_loader.PreparedFinder.find_spec { build_services }
    runtime.context --> server.sv_client._local_call { ExecutionContext }
    runtime.graph_utils --> server.session.project_database { get_name }
    runtime.prepared --> cli.commands.execution._load_executable | data.type_identity.resolve_type { load_prepared_module }
    runtime.prepared --> compiler.driver.application._prepare_revision { PreparedApplication, publish }
    runtime.prepared --> runtime.context.ExecutionContext.for_target { application_for, application_of }
    runtime.prepared --> runtime.runtime.JacModule.update_walker { application_for, module_builtins }
    runtime.prepared --> server.session.Session._materialize { application_for }
    runtime.prepared --> server.sv_client._local_call { application_of }
    type runtime.prepared --> data.type_identity { PreparedApplication }
    runtime.runtime --> cli.commands.execution._load_executable { JacRuntime as Jac }
    runtime.runtime --> runtime.context.ExecutionContext.bind_stream | runtime.prepared_loader.PreparedFinder.find_spec | server.sv_client._local_call { JacRuntime }
    runtime.constants --> compiler.backends.py.jcir_gen_pass.JcirGenPass._gen_native_interop_stubs { JAC_TO_CTYPES_STR }
    runtime.object_interop --> byllm.systemone._record_fields { fields as record_fields, is_record }
    runtime.object_interop --> byllm.systemone._state_value { fields as record_fields, is_record }
    runtime.semantic --> byllm.systemone { ClassInfo, EnumInfo, FunctionInfo, TypeForm, VarInfo }
    runtime.semantic --> byllm.tests.test_systemone { ClassInfo, EnumInfo, FieldInfo, FunctionInfo, ParamInfo, TypeForm }
    runtime.semantic --> compiler.driver.compiler { info_graph_from_json }
    runtime.semantic --> compiler.driver.unit_products { Info, info_graph_to_json }
    runtime.surface --> compiler.driver.unit_products { SurfaceEntry }
    runtime.archetype --> runtime.runtime { new_connect_edge }
    runtime.constructs --> server.server.ModuleIntrospector.target { WalkerArchetype }
    runtime.context --> server.request_scope { ExecutionContext }
    runtime.context --> server.task_scheduler.Scheduler._execute { CallState }
    runtime.exceptions --> server.session { TransactionLost }
    runtime.object_interop --> server.settings { fields, is_record }
    runtime.object_model --> scale.sso.oauth_session { asdict }
    runtime.osp_graph_sv --> server.session.Session._forget_loaded { sv_forget_edge }
    runtime.pass_link --> lib.jaclib { PassLink }
    runtime.preparation_lock --> compiler.driver.application.prepare_application { PREPARATION_LOCK }
    runtime.preparation_lock --> compiler.driver.application.prepare_dynamic_module { PREPARATION_LOCK }
    runtime.preparation_lock --> server.server.JacAPIServer._refresh_dev_endpoints { PREPARATION_LOCK }
    runtime.prepared --> compiler.driver.pipeline_runner.compile_application { holds_application_code }
    runtime.prepared --> runtime.prepared_loader.PreparedFinder.find_spec { module_index }
    runtime.prepared --> server.watcher.watch_roots { holds_application_code }
    runtime.region --> runtime.cinterop { escape_regions, restore_regions }
    runtime.runtime --> runtime.archetype._dirty_delattr | server.request_scope { JacRuntime }
    runtime.runtime --> server.server.ModuleIntrospector.route_spec { JacRuntime as Jac }
    runtime.scalars --> compiler.boundary_rules.json_refusal { sized_scalar_names }
    runtime.scalars --> compiler.boundary_rules.non_string_key { sized_scalar_names }
    runtime.scalars --> compiler.boundary_rules.python_native_wire { sized_scalar_names }
    runtime.preparation_lock --> runtime.runtime.JacModule.jac_import { PREPARATION_LOCK }
    runtime.preparation_lock --> server.hmr.HotReloader._reload_server_module { PREPARATION_LOCK }
    scale.admin --> scale.admin.admin_portal.JacAPIServerAdmin.build_admin_client { admin_portal }
    scale.admin --> scale.tests.misc.test_k8s_ops { k8s_ops }
    scale.admin as admin_pkg --> scale.tests.misc.test_ops_signals;
    scale.admin --> scale.tests.server.test_admin;
    scale.plugin --> cli.commands.execution._serve_fleet { scale_local_serve }
    comptime scale.plugin --> cli.manifest { SPEC_SCALE_CMD }
    scale.sdk --> scale.tests.deploy.sdk_deploy_driver { ProgressEvent, ScaleClient, deploy }
    scale.sdk --> scale.tests.deploy.test_superseded_deployment_reap { AutoscalerRuntimeStatus, AutoscalerTransition, ScaleClient }
    scale._optdeps.apscheduler --> scale.scheduler.scheduler { BackgroundScheduler, CronTrigger, HAS_APSCHEDULER }
    scale._optdeps.apscheduler --> scale.tests.misc.test_optional_deps;
    scale._optdeps.apscheduler --> scale.tests.misc.test_optional_deps { BackgroundScheduler, HAS_APSCHEDULER }
    scale._optdeps.firebase_auth --> scale.sso.firebase { HAS_FIREBASE_ADMIN, auth, credentials, firebase_admin }
    scale._optdeps.firebase_auth --> scale.tests.server.test_firebase_auth_sso { firebase_admin as _real_firebase_admin }
    scale._optdeps.gcs --> scale.storage.gcs_storage { NotFound, StorageClient, require_google_cloud_storage }
    scale._optdeps.gcs --> scale.tests.misc.test_optional_deps { HAS_GCS, StorageClient }
    scale._optdeps.kubernetes --> scale.admin.k8s_ops { HAS_KUBERNETES, client, config }
    scale._optdeps.kubernetes --> scale.deploy.autoscale.autoscaler.Autoscaler.read_workload { ApiException, client }
    scale._optdeps.kubernetes --> scale.deploy.autoscale.hpa_autoscaler { ApiException, AutoscalingV2Api, client }
    scale._optdeps.kubernetes --> scale.deploy.autoscale.http_activation_config { ApiException }
    scale._optdeps.kubernetes --> scale.deploy.autoscale.keda_autoscaler { ApiException, AutoscalingV2Api, client }
    scale._optdeps.kubernetes --> scale.deploy.autoscale.keda_autoscaler.KEDAAutoscaler.watch_scale_targets { watch }
    scale._optdeps.kubernetes --> scale.deploy.target.kubernetes.cluster_provider { client }
    scale._optdeps.kubernetes --> scale.deploy.target.kubernetes.database_provisioner { client }
    scale._optdeps.kubernetes --> scale.deploy.target.kubernetes.ingress { ApiException, client }
    scale._optdeps.kubernetes --> scale.deploy.target.kubernetes.kubernetes_target { ApiException, ConfigException, client, config as k8s_cluster_config }
    scale._optdeps.kubernetes --> scale.deploy.target.kubernetes.monitoring { ApiException, client }
    scale._optdeps.kubernetes --> scale.deploy.target.kubernetes.target { ApiException, client }
    scale._optdeps.kubernetes --> scale.deploy.target.kubernetes.utils.kubernetes_utils { ApiException, ConfigException, client, config }
    scale._optdeps.kubernetes --> scale.injector.pvc_injector.PvcInjector.seed { ApiException, client }
    scale._optdeps.kubernetes --> scale.tests.deploy.observer_transition_recorder { ApiException, config }
    scale._optdeps.kubernetes --> scale.tests.deploy.test_database_intent { ApiException }
    scale._optdeps.kubernetes --> scale.tests.misc.test_optional_deps;
    scale._optdeps.kubernetes --> scale.tests.misc.test_optional_deps { HAS_KUBERNETES, client as k8s_client }
    scale._optdeps.opentelemetry --> scale.admin.ops { HAS_OTEL }
    scale._optdeps.opentelemetry --> scale.runtime.context.tracing { HAS_OTEL }
    scale._optdeps.optional_deps --> scale._optdeps.gcs { require_optional }
    scale._optdeps.optional_deps --> scale._optdeps.opentelemetry { is_optional_available }
    scale._optdeps.optional_deps --> scale.config.project_env { require_optional }
    scale._optdeps.optional_deps --> scale.deploy.target.factory { require_optional }
    scale._optdeps.optional_deps --> scale.observability.factory { is_optional_available }
    scale._optdeps.optional_deps --> scale.sso.firebase { require_optional }
    scale._optdeps.optional_deps --> scale.tests.misc.test_optional_deps { is_optional_available, require_optional }
    scale._optdeps.prometheus --> scale.admin.ops { HAS_PROMETHEUS }
    scale._optdeps.prometheus --> scale.observability.prometheus_metrics { CONTENT_TYPE_LATEST, CollectorRegistry, Counter, Gauge, Histogram, generate_latest }
    scale._optdeps.prometheus --> scale.tests.misc.test_optional_deps;
    scale._optdeps.prometheus --> scale.tests.misc.test_optional_deps { Counter, HAS_PROMETHEUS }
    scale.admin.admin_portal --> scale.runtime.gateway.microservice_gateway { JacAPIServerAdmin }
    scale.admin.admin_portal --> scale.server.extensions { JacAPIServerAdmin }
    scale.admin.admin_portal --> scale.tests.misc.test_metrics { _calculate_metrics_summary, _classify_path, _parse_prometheus_text, _percentile_from_buckets }
    scale.admin.admin_portal --> scale.tests.misc.test_metrics._distribution_for { _calculate_metrics_summary, _parse_prometheus_text }
    scale.admin.deploy_health --> scale.runtime.gateway.microservice_gateway { JacAPIServerDeployHealth }
    scale.admin.deploy_health --> scale.server.extensions { JacAPIServerDeployHealth }
    scale.admin.deploy_health --> scale.tests.deploy.test_ops_deploy { JacAPIServerDeployHealth, summarize_deployment, summarize_pod }
    scale.admin.k8s_ops --> scale.admin.deploy_health { api_error_detail, apps_api, core_api, k8s_available, ops_namespace, unavailable_detail }
    scale.admin.k8s_ops --> scale.admin.network { api_error_detail, core_api, k8s_available, networking_api, ops_namespace, unavailable_detail }
    scale.admin.k8s_ops --> scale.admin.podenv { api_error_detail, core_api, k8s_available, ops_namespace, unavailable_detail }
    scale.admin.llm_telemetry --> scale.runtime.gateway.microservice_gateway { JacAPIServerLLMTelemetry }
    scale.admin.llm_telemetry --> scale.server.extensions { JacAPIServerLLMTelemetry }
    scale.admin.llm_telemetry --> scale.tests.misc.test_llm_telemetry { LLMCallRecord, TelemetryStore, Trace }
    scale.admin.logs --> scale.admin.ops { _app_namespace, _loki_base_url }
    scale.admin.logs --> scale.runtime.gateway.microservice_gateway { JacAPIServerLogs }
    scale.admin.logs --> scale.server.extensions { JacAPIServerLogs }
    scale.admin.logs --> scale.tests.server.test_admin_logs { JacAPIServerLogs, _build_logql, _flatten_loki_response, _service_to_pod_regex_for_mode, _services_for_mode }
    scale.admin.network --> scale.runtime.gateway.microservice_gateway { JacAPIServerNetwork }
    scale.admin.network --> scale.server.extensions { JacAPIServerNetwork }
    scale.admin.network --> scale.tests.deploy.test_ops_network { JacAPIServerNetwork, pvc_claimants, summarize_ingress, summarize_pvc, summarize_service }
    scale.admin.ops --> scale.runtime.gateway.microservice_gateway { JacAPIServerOps }
    scale.admin.ops --> scale.server.extensions { JacAPIServerOps }
    scale.admin.ops --> scale.tests.deploy.test_ops_health { JacAPIServerOps, _traces_chain, short_circuit_chain }
    scale.admin.podenv --> scale.runtime.gateway.microservice_gateway { JacAPIServerPodEnv }
    scale.admin.podenv --> scale.server.extensions { JacAPIServerPodEnv }
    scale.admin.podenv --> scale.tests.misc.test_ops_podenv { JacAPIServerPodEnv, pod_env_entries, redact_entry }
    scale.admin.service_urls --> scale.admin.logs { service_base_url }
    scale.admin.service_urls --> scale.admin.ops { service_base_url }
    scale.admin.service_urls --> scale.admin.traces { service_base_url }
    scale.admin.service_urls --> scale.tests.misc.test_service_urls { service_base_url }
    scale.admin.traces --> scale.admin.ops { _tempo_base_url }
    scale.admin.traces --> scale.runtime.gateway.microservice_gateway { JacAPIServerTraces }
    scale.admin.traces --> scale.server.extensions { JacAPIServerTraces }
    scale.admin.traces --> scale.tests.server.test_traces_admin { _build_traceql, _flatten_tempo_trace, _normalize_trace_id, _otlp_attrs, _otlp_value }
    scale.admin.workload_helpers --> scale.admin.workloads { match_owner, owner_name_from_pod, phase_to_status }
    scale.admin.workload_helpers --> scale.tests.server.test_admin_workloads { match_owner, owner_name_from_pod, phase_to_status }
    scale.admin.workloads --> scale.runtime.gateway.microservice_gateway { JacAPIServerWorkloads }
    scale.admin.workloads --> scale.server.extensions { JacAPIServerWorkloads }
    scale.admin.admin_portal --> scale.tests.server.test_auth_policy_startup { JacAPIServerAdmin }
    scale.config.app_config --> scale.deploy.target.deployment_target { AppConfig }
    scale.config.app_config --> scale.deploy.target.kubernetes.manifest_builder { AppConfig }
    scale.config.app_config --> scale.deploy.target.kubernetes.target { AppConfig }
    scale.config.app_config --> scale.plugin { deployed_tree }
    scale.config.app_config --> scale.runtime.cli.plan { AppConfig }
    scale.config.app_config --> scale.runtime.realizer.kubernetes_realizer { AppConfig, deployed_tree }
    scale.config.app_config --> scale.sdk.client { AppConfig, deployed_tree }
    scale.config.app_config --> scale.tests.apps.test_app_scale_overrides { AppConfig }
    scale.config.app_config --> scale.tests.deploy.test_access_hint { AppConfig }
    scale.config.app_config --> scale.tests.deploy.test_alb_zero_downtime { AppConfig }
    scale.config.app_config --> scale.tests.deploy.test_deploy_banner { deployed_tree }
    scale.config.app_config --> scale.tests.deploy.test_deploy_k8s { AppConfig }
    scale.config.app_config --> scale.tests.deploy.test_dry_run_purity { AppConfig }
    scale.config.app_config --> scale.tests.deploy.test_factories { AppConfig }
    scale.config.app_config --> scale.tests.deploy.test_http_activation_microservices { AppConfig }
    scale.config.app_config --> scale.tests.deploy.test_memory_trigger_guard { AppConfig }
    scale.config.app_config --> scale.tests.deploy.test_pdb_budget { AppConfig }
    scale.config.app_config --> scale.tests.deploy.test_pod_env { AppConfig }
    scale.config.app_config --> scale.tests.deploy.test_show_yaml_autoscalers { AppConfig }
    scale.config.app_config --> scale.tests.deploy.test_superseded_deployment_reap { AppConfig }
    scale.config.app_config --> scale.tests.deploy.test_version_pin { AppConfig }
    scale.config.base_config --> scale.deploy.target.deployment_target { BaseConfig }
    scale.config.base_config --> scale.deploy.target.kubernetes.kubernetes_config { BaseConfig }
    scale.config.config_loader --> scale.admin.admin_portal { get_scale_config }
    scale.config.config_loader --> scale.admin.llm_telemetry.JacAPIServerLLMTelemetry.register_llm_telemetry_endpoints { get_scale_config }
    scale.config.config_loader --> scale.admin.logs { get_scale_config }
    scale.config.config_loader --> scale.admin.ops { get_scale_config }
    scale.config.config_loader --> scale.admin.service_urls { get_scale_config }
    scale.config.config_loader --> scale.admin.traces { get_scale_config }
    scale.config.config_loader --> scale.admin.workloads._metrics_namespace { get_scale_config }
    scale.config.config_loader --> scale.admin.workloads._unavailable_reason { get_scale_config }
    scale.config.config_loader --> scale.deploy.database.kubernetes_postgres { get_scale_config }
    scale.config.config_loader --> scale.deploy.target.kubernetes.kubernetes_target { get_scale_config }
    scale.config.config_loader --> scale.deploy.target.kubernetes.manifest_builder { GATEWAY_POD_KEYS, get_scale_config, normalize_gateway_config }
    scale.config.config_loader --> scale.deploy.target.kubernetes.runtime_resolver.resolve_peer_route { get_scale_config }
    scale.config.config_loader --> scale.deploy.target.kubernetes.target { get_scale_config }
    scale.config.config_loader --> scale.deploy.target.kubernetes.target.KubernetesTarget._gateway_cfg { normalize_gateway_config }
    scale.config.config_loader --> scale.plugin { get_scale_config }
    scale.config.config_loader --> scale.runtime.cli.diagnostics.PlanValidator._check_config_keys { get_scale_config }
    scale.config.config_loader --> scale.runtime.context.log_emit.install_structured_logging { peek_scale_config }
    scale.config.config_loader --> scale.runtime.context.util.boot_health_timeout { get_scale_config }
    scale.config.config_loader --> scale.runtime.context.util.http_forward_timeout { get_scale_config }
    scale.config.config_loader --> scale.runtime.context.util.route_refresh_seconds { get_scale_config }
    scale.config.config_loader --> scale.runtime.fleet._build_fleet { app_scale_overrides }
    scale.config.config_loader --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.setup { get_scale_config }
    scale.config.config_loader --> scale.runtime.provider { get_scale_config }
    scale.config.config_loader --> scale.runtime.provider.JacScaleRuntime.get_sv_service_routes { get_scale_config }
    scale.config.config_loader --> scale.runtime.realizer.kubernetes_realizer { get_scale_config }
    scale.config.config_loader --> scale.runtime.rpc.rpc._sv_rpc_timeout { get_scale_config }
    scale.config.config_loader --> scale.scheduler.scheduler { get_scale_config }
    scale.config.config_loader --> scale.server.extensions { get_scale_config }
    scale.config.config_loader --> scale.server.jobs_ext { get_scale_config }
    scale.config.config_loader --> scale.server.sso_ext { get_scale_config }
    scale.config.config_loader --> scale.server.webhook_ext { get_scale_config }
    scale.config.config_loader --> scale.server.websocket_ext { get_scale_config }
    scale.config.config_loader --> scale.sso.sso_auth { get_scale_config }
    scale.config.config_loader --> scale.tests.apps.test_app_scale_overrides { APP_SCALE_KEYS, JacScaleConfig, app_scale_overrides, get_scale_config, normalize_gateway_config, reset_scale_config }
    scale.config.config_loader --> scale.tests.data.test_firebase_env { get_scale_config, reset_scale_config }
    scale.config.config_loader --> scale.tests.data.test_gateway_owned_identity { normalize_gateway_config }
    scale.config.config_loader --> scale.tests.deploy.test_client_build_stage { get_scale_config, reset_scale_config }
    scale.config.config_loader --> scale.tests.deploy.test_database_intent { get_scale_config, reset_scale_config }
    scale.config.config_loader --> scale.tests.deploy.test_deploy_k8s { JacScaleConfig, get_scale_config, reset_scale_config }
    scale.config.config_loader --> scale.tests.deploy.test_deployment_overlay { JacScaleConfig }
    scale.config.config_loader --> scale.tests.deploy.test_gateway_config_isolation { get_scale_config, reset_scale_config }
    scale.config.config_loader as config_loader_mod --> scale.tests.deploy.test_pod_env;
    scale.config.config_loader --> scale.tests.deploy.test_pod_env { reset_scale_config }
    scale.config.config_loader --> scale.tests.deploy.test_service_routing { get_scale_config, reset_scale_config }
    scale.config.config_loader --> scale.tests.microservices.test_binary_injector { JacScaleConfig }
    scale.config.config_loader as cfg_mod --> scale.tests.microservices.test_gateway;
    scale.config.config_loader as config_loader --> scale.tests.microservices.test_gateway._with_cors_config;
    scale.config.config_loader --> scale.tests.misc.test_config_loader { JacScaleConfig, get_scale_config, reset_scale_config }
    scale.config.config_loader --> scale.tests.misc.test_config_validation { JacScaleConfig, get_scale_config, normalize_gateway_config, reset_scale_config }
    scale.config.config_loader --> scale.tests.misc.test_log_emit { get_scale_config, peek_scale_config, reset_scale_config }
    scale.config.config_loader --> scale.tests.misc.test_service_urls { get_scale_config, reset_scale_config }
    scale.config.config_loader --> scale.tests.misc.test_shared_store_failure { get_scale_config, reset_scale_config }
    scale.config.config_loader --> scale.tests.server.test_firebase_auth_sso { reset_scale_config }
    scale.config.config_loader --> scale.tests.server.test_scheduler_endpoints { get_scale_config, reset_scale_config }
    scale.config.config_loader as config_loader_mod --> scale.tests.server.test_sv_auth_forward;
    scale.config.config_loader --> scale.tests.server.test_webhook { get_scale_config, reset_scale_config }
    scale.config.config_loader --> scale.tests.server.test_ws_hardening { _ws_positive, get_scale_config, reset_scale_config }
    scale.config.config_loader --> scale.webhook.webhook { get_scale_config }
    scale.config.config_loader --> server.shared_store.scale_db_url { get_scale_config }
    scale.config.dev_config --> scale.deploy.target.kubernetes.target.KubernetesTarget.deploy { resolve_dev_channel }
    scale.config.dev_config --> scale.injector.binary.deploy_generation_refusal { Channel, resolve_dev_channel }
    scale.config.dev_config --> scale.injector.binary.host_toolchain_path { resolve_dev_channel }
    scale.config.dev_config --> scale.injector.binary.preflight_pod_runtime { Channel }
    scale.config.dev_config --> scale.injector.binary.resolve_console_version { Channel }
    scale.config.dev_config --> scale.injector.binary.resolve_deploy_version { Channel }
    scale.config.dev_config --> scale.injector.binary.resolve_pod_base_image { Channel, resolve_dev_channel, resolve_experimental_pr, resolve_pinned_spec }
    scale.config.dev_config --> scale.injector.binary_injector { Channel }
    scale.config.dev_config --> scale.injector.binary_injector.select_injector { resolve_dev_channel }
    scale.config.dev_config --> scale.tests.microservices.test_binary_injector { Channel, resolve_dev_channel, resolve_experimental_pr }
    scale.config.firebase_env --> scale.config.config_loader { FIREBASE_AUTH_PROJECT_ID_ENV, FIRESTORE_PROJECT_ID_ENV, resolve_firebase_project_id }
    scale.config.firebase_env --> scale.sso.firebase { firebase_project_id_env_hint }
    scale.config.firebase_env --> scale.sso.sso_auth { firebase_project_id_env_hint }
    scale.config.firebase_env --> scale.storage.factory { JAC_STORAGE_FIREBASE_PROJECT_ID_ENV, JAC_STORAGE_GCS_PROJECT_ID_ENV, resolve_firebase_project_id }
    scale.config.firebase_env --> scale.tests.data.test_firebase_env { FIREBASE_AUTH_PROJECT_ID_ENV, FIREBASE_PROJECT_ID_ENV, FIRESTORE_PROJECT_ID_ENV, JAC_STORAGE_FIREBASE_PROJECT_ID_ENV, resolve_firebase_project_id }
    scale.config.plugin_config --> scale.config.config_loader.JacScaleConfig.get_app_config_schema { app_scale_schema }
    scale.config.plugin_config --> scale.config.validation { JacScalePluginConfig, app_scale_schema }
    scale.config.plugin_config --> scale.tests.misc.test_config_loader { JacScalePluginConfig }
    scale.config.plugin_config --> scale.tests.misc.test_config_validation { JacScalePluginConfig }
    scale.config.project_env --> scale.plugin { load_project_env }
    scale.config.project_env --> scale.runtime.realizer.kubernetes_realizer { load_project_env }
    scale.config.project_env --> scale.tests.misc.test_optional_deps { PROJECT_ENV_CAPABILITY, project_env_path }
    scale.config.validation --> scale.config.config_loader.JacScaleConfig.get_config_schema { scale_schema_options }
    scale.config.validation --> scale.config.config_loader.JacScaleConfig.get_config_strict_env { STRICT_ENV }
    scale.config.validation --> scale.config.config_loader.JacScaleConfig.get_scheduler_config { scheduler_job_cap, scheduler_min_interval }
    scale.config.validation --> scale.config.config_loader.app_scale_overrides { STRICT_ENV, validate_app_scale_config }
    scale.config.validation --> scale.runtime.cli.diagnostics.PlanValidator._check_config_keys { validate_scale_config }
    scale.config.validation --> scale.tests.apps.test_app_scale_overrides { STRICT_ENV, validate_app_scale_config, validate_scale_config }
    scale.config.validation --> scale.tests.misc.test_config_validation { STRICT_ENV, known_deploy_targets, scheduler_job_cap, scheduler_min_interval, validate_scale_config }
    scale.config.config_loader --> scale.tests.deploy.test_deployment_overlay { get_scale_config, reset_scale_config }
    scale.config.config_loader --> scale.deploy.target.kubernetes.manifest_builder { ADMIN_PASSWORD_ENV, SIGNING_SECRET_ENV }
    scale.config.config_loader --> scale.deploy.target.kubernetes.target { ADMIN_PASSWORD_ENV, SIGNING_SECRET_ENV }
    scale.config.config_loader --> scale.emailer.factory.configured { get_scale_config }
    scale.config.config_loader --> scale.runtime.context.service_routing.is_http_activated { get_scale_config }
    scale.config.config_loader --> scale.server.extensions { ADMIN_PASSWORD_ENV }
    scale.config.config_loader --> scale.tests.microservices.test_gateway { get_scale_config, reset_scale_config }
    scale.config.dev_config --> scale.injector.binary.read_local_binary { local_pod_binary }
    scale.deploy.autoscale.autoscaler --> scale.deploy.autoscale.factory { Autoscaler }
    scale.deploy.autoscale.autoscaler --> scale.deploy.autoscale.hpa_autoscaler { Autoscaler, AutoscalerRuntimeStatus, AutoscalerSpec, DEFAULT_CPU_UTILIZATION_TARGET, DEFAULT_MEMORY_UTILIZATION_TARGET, condition, normalize_conditions, tristate }
    scale.deploy.autoscale.autoscaler --> scale.deploy.autoscale.keda_autoscaler { Autoscaler, AutoscalerRuntimeStatus, AutoscalerSpec, AutoscalerTransition, DEFAULT_CPU_UTILIZATION_TARGET, DEFAULT_MEMORY_UTILIZATION_TARGET, Trigger, TriggerAuth, condition, normalize_conditions, transition_from, tristate }
    scale.deploy.autoscale.autoscaler --> scale.deploy.target.kubernetes.target { AutoscalerSpec, Trigger, TriggerAuth }
    scale.deploy.autoscale.autoscaler --> scale.sdk { AutoscalerRuntimeStatus, AutoscalerTransition }
    scale.deploy.autoscale.autoscaler --> scale.sdk.client { AutoscalerRuntimeStatus, AutoscalerTransition }
    scale.deploy.autoscale.autoscaler --> scale.tests.deploy.test_deploy_k8s { AutoscalerSpec, Trigger }
    scale.deploy.autoscale.autoscaler --> scale.tests.deploy.test_deployment_overlay { Autoscaler, AutoscalerSpec }
    scale.deploy.autoscale.autoscaler --> scale.tests.deploy.test_factories { AutoscalerSpec, Trigger }
    scale.deploy.autoscale.autoscaler --> scale.tests.deploy.test_http_activation_microservices { AutoscalerSpec, Trigger, TriggerAuth }
    scale.deploy.autoscale.factory --> scale.deploy.target.kubernetes.target { AutoscalerFactory }
    scale.deploy.autoscale.factory --> scale.sdk.client { AutoscalerFactory }
    scale.deploy.autoscale.factory --> scale.tests.deploy.test_deploy_k8s { AutoscalerFactory }
    scale.deploy.autoscale.factory --> scale.tests.deploy.test_factories { AutoscalerFactory }
    scale.deploy.autoscale.factory --> scale.tests.deploy.test_service_routing { AutoscalerFactory }
    scale.deploy.autoscale.hpa_autoscaler --> scale.deploy.autoscale.factory.AutoscalerFactory.create { HPAAutoscaler }
    scale.deploy.autoscale.hpa_autoscaler --> scale.tests.deploy.test_factories { HPAAutoscaler }
    scale.deploy.autoscale.http_activation --> scale.deploy.autoscale.http_activation_config { HTTPActivationSpec, HTTPColdStartSpec, HTTPConcurrencyMetric, HTTPHeaderMatch, HTTPPathMatch, HTTPRequestRateMetric, HTTPRoutingRule, HTTPServiceTarget, HTTPStaticResponse, HTTPTimeoutSpec }
    scale.deploy.autoscale.http_activation --> scale.deploy.autoscale.keda_autoscaler { HTTPActivationSpec, HTTPRoutingRule }
    scale.deploy.autoscale.http_activation --> scale.tests.deploy.http_activation_test_support { HTTPActivationSpec, HTTPConcurrencyMetric, HTTPServiceTarget }
    scale.deploy.autoscale.http_activation --> scale.tests.deploy.test_http_activation_microservices { HTTPColdStartSpec, HTTPHeaderMatch, HTTPPathMatch, HTTPRequestRateMetric, HTTPRoutingRule, HTTPServiceTarget, HTTPStaticResponse, HTTPTimeoutSpec }
    scale.deploy.autoscale.http_activation_config --> scale.deploy.target.kubernetes.manifest_builder { build_http_activation_spec }
    scale.deploy.autoscale.http_activation_config --> scale.deploy.target.kubernetes.target { apply_http_activation_for_target, destroy_http_activation_for_target }
    scale.deploy.autoscale.http_activation_config --> scale.tests.deploy.test_http_activation_config { apply_http_activation_for_target, build_http_activation_spec, destroy_http_activation_for_target }
    scale.deploy.autoscale.keda_autoscaler --> scale.deploy.autoscale.factory.AutoscalerFactory.create { KEDAAutoscaler }
    scale.deploy.autoscale.keda_autoscaler --> scale.deploy.autoscale.http_activation_config { KEDAAutoscaler }
    scale.deploy.autoscale.keda_autoscaler --> scale.deploy.target.kubernetes.target { KEDAAutoscaler }
    scale.deploy.autoscale.keda_autoscaler --> scale.tests.deploy.http_activation_test_support { KEDAAutoscaler }
    scale.deploy.autoscale.keda_autoscaler --> scale.tests.deploy.observer_transition_recorder { KEDAAutoscaler }
    scale.deploy.autoscale.keda_autoscaler --> scale.tests.deploy.test_factories { KEDAAutoscaler }
    scale.deploy.autoscale.keda_autoscaler --> scale.tests.deploy.test_http_activation_config { KEDAAutoscaler }
    scale.deploy.autoscale.keda_autoscaler --> scale.tests.deploy.test_http_activation_microservices { KEDAAutoscaler }
    scale.deploy.autoscale.keda_autoscaler --> scale.tests.deploy.test_service_routing { KEDAAutoscaler }
    scale.deploy.autoscale.keda_capabilities --> scale.deploy.autoscale.keda_autoscaler { KEDACapabilities, SUPPORTED_HTTP_INTERCEPTOR_API_VERSIONS }
    scale.deploy.database.kubernetes_postgres --> scale.deploy.target.kubernetes.kubernetes_target { KubernetesPostgresProvider }
    scale.deploy.database.kubernetes_postgres --> scale.tests.deploy.test_deploy_k8s { KubernetesPostgresProvider }
    scale.deploy.database.kubernetes_postgres --> scale.tests.deploy.test_postgres_predicate_lock_headroom { KubernetesPostgresProvider }
    scale.deploy.target.deployment_target --> scale.deploy.database.kubernetes_postgres { DeploymentTarget }
    scale.deploy.target.deployment_target --> scale.deploy.target.factory { DeploymentTarget }
    scale.deploy.target.deployment_target --> scale.deploy.target.kubernetes.kubernetes_target { DeploymentTarget }
    type scale.deploy.target.deployment_target --> scale.deploy.target.registry { DeploymentTarget }
    scale.deploy.target.factory --> scale.plugin { DeploymentTargetFactory }
    scale.deploy.target.factory --> scale.runtime.realizer.kubernetes_realizer { DeploymentTargetFactory }
    scale.deploy.target.factory --> scale.sdk.client { ensure_deploy_tooling, require_deploy_tooling }
    scale.deploy.target.factory --> scale.tests.deploy.test_deploy_banner { DeploymentTargetFactory }
    scale.deploy.target.factory --> scale.tests.deploy.test_deploy_k8s { DeploymentTargetFactory }
    scale.deploy.target.factory --> scale.tests.deploy.test_dry_run_purity { DeploymentTargetFactory }
    scale.deploy.target.factory --> scale.tests.deploy.test_factories { DeploymentTargetFactory }
    scale.deploy.target.factory --> scale.tests.misc.test_config_validation { DeploymentTargetFactory }
    scale.deploy.target.factory --> scale.tests.misc.test_optional_deps { DeploymentTargetFactory }
    scale.deploy.target.registry --> scale.config.validation { DeploymentTargetRegistry }
    scale.deploy.target.registry --> scale.deploy.target.factory { DeploymentTargetRegistry }
    scale.deploy.target.registry --> scale.tests.misc.test_config_validation { BUILTIN_TARGET_TYPES }
    scale.deploy.target.service_deployer --> scale.deploy.target.kubernetes.runtime_resolver { ServiceDeployer }
    scale.deploy.target.service_deployer --> scale.runtime.orchestrator.local_deployer { ServiceDeployer }
    scale.deploy.target.service_deployer --> scale.runtime.orchestrator.process_manager { ServiceDeployer }
    scale.deploy.target.kubernetes.cluster_provider --> scale.deploy.target.kubernetes.ingress { ClusterProvider }
    scale.deploy.target.kubernetes.cluster_provider --> scale.deploy.target.kubernetes.monitoring { ClusterProvider }
    scale.deploy.target.kubernetes.cluster_provider --> scale.deploy.target.kubernetes.utils.kubernetes_utils { AWSProvider, ClusterProvider, LocalProvider }
    scale.deploy.target.kubernetes.cluster_provider --> scale.tests.deploy.test_cluster_provider { AWSProvider, LocalProvider }
    scale.deploy.target.kubernetes.database_provisioner --> scale.deploy.target.kubernetes.target { DatabaseProvisioner }
    scale.deploy.target.kubernetes.database_provisioner --> scale.tests.deploy.test_pod_env { DatabaseProvisioner }
    scale.deploy.target.kubernetes.ingress --> scale.deploy.target.kubernetes.kubernetes_target { IngressDeployer }
    scale.deploy.target.kubernetes.ingress --> scale.tests.deploy.test_deploy_k8s { IngressDeployer }
    scale.deploy.target.kubernetes.ingress --> scale.tests.deploy.test_ingress_deployer { IngressDeployer }
    scale.deploy.target.kubernetes.ingress --> scale.tests.deploy.test_ingress_tls_preservation { IngressDeployer }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.config.config_loader.JacScaleConfig.get_kubernetes_config { KubernetesConfig, k8s_safe_slug }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.deploy.database.kubernetes_postgres.KubernetesPostgresProvider._requested_mode { resolve_database_mode }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.deploy.target.factory.DeploymentTargetFactory.create { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.deploy.target.kubernetes.ingress { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.deploy.target.kubernetes.kubernetes_target { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.deploy.target.kubernetes.manifest_builder { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.deploy.target.kubernetes.monitoring { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.deploy.target.kubernetes.runtime_bootstrap { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.deploy.target.kubernetes.target { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.sdk.client { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.sdk.spec.DeploySpec.from_config { k8s_safe_slug }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.sdk.spec.DeploySpec.to_target_config { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.apps.test_app_scale_overrides { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_access_hint { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_alb_zero_downtime { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_client_build_deps { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_client_build_fail_fast { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_client_build_stage { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_crash_scan_fleet_guard { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_database_intent { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_deploy_k8s { KubernetesConfig, k8s_safe_slug }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_deployment_overlay { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_destroy_reclaim { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_dry_run_purity { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_factories { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_gateway_config_isolation { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_http_activation_microservices { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_ingress_deployer { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_ingress_tls_preservation { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_memory_trigger_guard { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_monitoring_switch { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_pdb_budget { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_pod_env { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_service_routing { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_show_yaml_autoscalers { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_superseded_deployment_reap { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.deploy.test_version_pin { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.microservices.test_binary_injector { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.microservices.test_fleet_rollout { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.misc.test_config_loader { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.misc.test_config_validation { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.misc.test_k8s_config_tracing { KubernetesConfig }
    scale.deploy.target.kubernetes.kubernetes_target --> scale.deploy.target.kubernetes.target { KubernetesTargetBase }
    scale.deploy.target.kubernetes.kubernetes_target --> scale.runtime.realizer.kubernetes_realizer.KubernetesRealizer.realize { KubernetesTargetBase }
    scale.deploy.target.kubernetes.kubernetes_target --> scale.tests.deploy.test_database_intent { KubernetesTargetBase }
    scale.deploy.target.kubernetes.manifest_builder --> scale.deploy.autoscale.autoscaler.Autoscaler._build_behavior { merge_manifest_overlay }
    scale.deploy.target.kubernetes.manifest_builder --> scale.deploy.target.kubernetes.target { CONFIG_REVISION_ANNOTATION, ManifestBuilder, ScalingMode, with_config_revision }
    scale.deploy.target.kubernetes.manifest_builder --> scale.runtime.cli.diagnostics { ScalingMode }
    scale.deploy.target.kubernetes.manifest_builder --> scale.runtime.cli.plan { ScalingMode }
    scale.deploy.target.kubernetes.manifest_builder --> scale.tests.apps.test_app_scale_overrides { ManifestBuilder }
    scale.deploy.target.kubernetes.manifest_builder --> scale.tests.deploy.test_access_hint { ManifestBuilder }
    scale.deploy.target.kubernetes.manifest_builder --> scale.tests.deploy.test_alb_zero_downtime { ManifestBuilder }
    scale.deploy.target.kubernetes.manifest_builder --> scale.tests.deploy.test_client_build_deps { ManifestBuilder }
    scale.deploy.target.kubernetes.manifest_builder --> scale.tests.deploy.test_client_build_fail_fast { ManifestBuilder }
    scale.deploy.target.kubernetes.manifest_builder --> scale.tests.deploy.test_client_build_stage { ManifestBuilder, _CLIENT_BUILD_ATTEMPTS, _CLIENT_BUILD_RETRY_PAUSE_S, _is_transient_client_build_failure, _membership_diagnosis }
    scale.deploy.target.kubernetes.manifest_builder --> scale.tests.deploy.test_deployment_overlay { CONFIG_REVISION_ANNOTATION, ManifestBuilder, merge_manifest_overlay, with_config_revision }
    scale.deploy.target.kubernetes.manifest_builder --> scale.tests.deploy.test_dry_run_purity { ManifestBuilder }
    scale.deploy.target.kubernetes.manifest_builder --> scale.tests.deploy.test_gateway_config_isolation { ManifestBuilder }
    scale.deploy.target.kubernetes.manifest_builder --> scale.tests.deploy.test_http_activation_microservices { ManifestBuilder, ScalingMode }
    scale.deploy.target.kubernetes.manifest_builder --> scale.tests.deploy.test_memory_trigger_guard { ManifestBuilder }
    scale.deploy.target.kubernetes.manifest_builder --> scale.tests.deploy.test_pdb_budget { ManifestBuilder, ScalingMode, pdb_spec }
    scale.deploy.target.kubernetes.manifest_builder --> scale.tests.deploy.test_pod_env { CONFIG_REVISION_ANNOTATION, ManifestBuilder, with_config_revision }
    scale.deploy.target.kubernetes.manifest_builder --> scale.tests.deploy.test_service_routing { ManifestBuilder }
    scale.deploy.target.kubernetes.manifest_builder --> scale.tests.deploy.test_show_yaml_autoscalers { ManifestBuilder, ScalingMode }
    scale.deploy.target.kubernetes.manifest_builder --> scale.tests.deploy.test_superseded_deployment_reap { ManifestBuilder }
    scale.deploy.target.kubernetes.monitoring --> scale.deploy.target.kubernetes.target { MonitoringDeployer }
    scale.deploy.target.kubernetes.ops_rbac --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder.generate_manifests { build_ops_rbac }
    scale.deploy.target.kubernetes.ops_rbac --> scale.tests.deploy.test_ops_rbac { build_ops_rbac, ops_role_name }
    scale.deploy.target.kubernetes.runtime_bootstrap --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._build_pod_spec { build_bootstrap_init_container, image_pull_policy, runtime_container_env }
    scale.deploy.target.kubernetes.runtime_bootstrap --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._pod_entrypoint { build_service_apt_prefix }
    scale.deploy.target.kubernetes.runtime_bootstrap --> scale.tests.microservices.test_binary_injector { build_bootstrap_init_container, build_runtime_install_commands, build_service_apt_prefix, image_pull_policy, runtime_container_env }
    scale.deploy.target.kubernetes.runtime_resolver --> scale.runtime.provider.JacScaleRuntime.get_sv_service_routes { build_k8s_registry_routes }
    scale.deploy.target.kubernetes.runtime_resolver as resolver_mod --> scale.tests.deploy.test_pod_env;
    scale.deploy.target.kubernetes.runtime_resolver --> scale.tests.deploy.test_pod_env { K8sRuntimeServiceResolver, build_k8s_registry, resolve_peer_route }
    scale.deploy.target.kubernetes.runtime_resolver --> scale.tests.deploy.test_service_routing { build_k8s_registry_routes }
    scale.deploy.target.kubernetes.target --> scale.deploy.target.factory.DeploymentTargetFactory.create { KubernetesTarget }
    scale.deploy.target.kubernetes.target --> scale.runtime.realizer.kubernetes_realizer.KubernetesRealizer.realize { KubernetesTarget }
    scale.deploy.target.kubernetes.target --> scale.sdk.client { KubernetesTarget }
    scale.deploy.target.kubernetes.target --> scale.tests.deploy.test_access_hint { KubernetesTarget }
    scale.deploy.target.kubernetes.target --> scale.tests.deploy.test_alb_zero_downtime { KubernetesTarget }
    scale.deploy.target.kubernetes.target --> scale.tests.deploy.test_crash_scan_fleet_guard { KubernetesTarget }
    scale.deploy.target.kubernetes.target --> scale.tests.deploy.test_http_activation_microservices { KubernetesTarget, apply_http_activations_for_bundle, reap_stale_scaling_resources_for_bundle }
    scale.deploy.target.kubernetes.target --> scale.tests.deploy.test_memory_trigger_guard { KubernetesTarget }
    scale.deploy.target.kubernetes.target --> scale.tests.deploy.test_monitoring_switch { KubernetesTarget }
    scale.deploy.target.kubernetes.target --> scale.tests.deploy.test_pod_env { KubernetesTarget }
    scale.deploy.target.kubernetes.target --> scale.tests.deploy.test_show_yaml_autoscalers { KubernetesTarget }
    scale.deploy.target.kubernetes.target as target_mod --> scale.tests.deploy.test_superseded_deployment_reap;
    scale.deploy.target.kubernetes.target --> scale.tests.deploy.test_superseded_deployment_reap { KubernetesTarget, app_bundle_digest, fleet_revert_order, fleet_targets_for_release, releases_from_revisions, restorable_pod_template }
    scale.deploy.target.kubernetes.target --> scale.tests.deploy.test_version_pin { KubernetesTarget }
    scale.deploy.target.kubernetes.target --> scale.tests.microservices.test_fleet_rollout { KubernetesTarget }
    scale.deploy.target.kubernetes.kubernetes_config --> scale.tests.microservices.test_pvc_injector { KubernetesConfig }
    scale.deploy.target.kubernetes.runtime_bootstrap --> scale.tests.microservices.test_pvc_injector { build_bootstrap_init_container }
    scale.deploy.target.kubernetes.target --> scale.tests.deploy.test_http_activation_microservices { replacing_init_containers }
    scale.deploy.target.kubernetes.utils.kubernetes_utils --> scale.deploy.autoscale.hpa_autoscaler { delete_if_exists }
    scale.deploy.target.kubernetes.utils.kubernetes_utils --> scale.deploy.target.kubernetes.database_provisioner { ensure_namespace_exists }
    scale.deploy.target.kubernetes.utils.kubernetes_utils --> scale.deploy.target.kubernetes.ingress { delete_if_exists }
    scale.deploy.target.kubernetes.utils.kubernetes_utils --> scale.deploy.target.kubernetes.kubernetes_target { COMPANION_DEFS, create_k8s_secret, get_cluster_provider, resize_pvc_if_needed }
    scale.deploy.target.kubernetes.utils.kubernetes_utils --> scale.deploy.target.kubernetes.monitoring { delete_if_exists, delete_k8s_secret }
    scale.deploy.target.kubernetes.utils.kubernetes_utils --> scale.deploy.target.kubernetes.target { PSS_ENFORCE_LABEL, _refresh_rs_hashes, _resolve_current_rs_hashes, create_k8s_secret, delete_if_exists, delete_k8s_secret, delete_namespace, ensure_namespace_exists, get_cluster_provider, namespace_is_owned, privileged_pss_labels }
    scale.deploy.target.kubernetes.utils.kubernetes_utils --> scale.deploy.target.kubernetes.target.KubernetesTarget._pod_failure_detail { describe_pod_status }
    scale.deploy.target.kubernetes.utils.kubernetes_utils --> scale.injector.pvc_injector.PvcInjector.seed { run_kubectl_command, wait_for_pod_deletion, wait_for_pod_phase }
    scale.deploy.target.kubernetes.utils.kubernetes_utils --> scale.tests.deploy.test_cluster_provider { get_cluster_provider }
    scale.deploy.target.kubernetes.utils.kubernetes_utils --> scale.tests.deploy.test_k8s_utils { parse_storage_quantity, resize_pvc_if_needed }
    scale.deploy.target.kubernetes.utils.kubernetes_utils --> scale.tests.deploy.test_pod_env { create_k8s_secret }
    scale.deploy.target.kubernetes.utils.kubernetes_utils --> scale.tests.deploy.test_pss_labels { PSS_ENFORCE_LABEL, PSS_SOURCE_LABEL, PSS_WARN_LABEL, default_pss_labels, privileged_pss_labels }
    scale.deploy.target.kubernetes.utils.kubernetes_utils --> scale.deploy.target.kubernetes.target { resolve_minted_secret }
    scale.deploy.target.kubernetes.utils.kubernetes_utils --> scale.tests.deploy.test_pod_env { resolve_minted_secret }
    scale.emailer.emailer --> scale.emailer.emailers { Emailer }
    scale.emailer.emailer --> scale.emailer.factory { Emailer }
    scale.emailer.emailer --> scale.server.extensions { Emailer }
    scale.emailer.emailer --> scale.tests.server.test_emailer_factory { Emailer }
    scale.emailer.emailers --> scale.emailer.factory.create { SMTPEmailer }
    scale.emailer.emailers --> scale.tests.server.test_emailer_factory { SMTPEmailer }
    scale.emailer.factory --> scale.tests.server.test_emailer_factory { create as create_emailer, register }
    scale.emailer.emailer --> scale.emailer.emailers { EmailAttachment }
    scale.emailer.emailer --> scale.tests.server.test_emailer_factory { EmailAttachment }
    scale.emailer.factory --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway._install_admin_api { configured as configured_emailer }
    scale.emailer.factory --> scale.server.extensions { configured as configured_emailer }
    scale.events.broker --> scale.config.config_loader.JacScaleConfig.get_events_config { RetryPolicy }
    scale.events.broker --> scale.events.publisher { Event, EventStreamBroker }
    scale.events.broker --> scale.events.streams._stream_common { Event, RetryPolicy, StreamPosition }
    scale.events.broker --> scale.events.streams.local { Event, EventStreamBroker, HealthStatus, RetryPolicy, StreamPosition, starts_at_earliest }
    scale.events.broker --> scale.events.streams.postgres { Event, EventStreamBroker, HealthStatus, RetryPolicy, StreamPosition, starts_at_earliest }
    scale.events.broker --> scale.events.subscriber { Event, RetryPolicy, StreamPosition }
    scale.events.broker --> scale.tests.data.test_local_stream { Event, RetryPolicy }
    scale.events.broker --> scale.tests.data.test_pg_stream { Event }
    scale.events.broker --> scale.tests.misc.test_events { Event, EventStreamBroker, HealthStatus, RetryPolicy, StreamPosition, starts_at_earliest }
    scale.events.publisher --> scale.server.extensions.EventsExtension.register { set_broker }
    scale.events.publisher --> scale.tests.misc.test_events { publish, set_broker }
    scale.events.subscriber --> scale.server.extensions.EventsExtension.register { get_subscriptions }
    scale.events.subscriber --> scale.tests.misc.test_events { get_subscriptions, subscribe }
    scale.events.streams._stream_common --> scale.events.streams.local { consumer_loop, wait_or_stop }
    scale.events.streams._stream_common --> scale.tests.misc.test_events { consumer_loop }
    scale.events.streams.local --> scale.server.extensions.EventsExtension.register { LocalEventStream }
    scale.events.streams.local --> scale.tests.data.test_local_stream { LocalEventStream }
    scale.events.streams.local --> scale.tests.misc.test_events { LocalEventStream }
    scale.events.streams.postgres --> scale.runtime.provider { PgEventStream }
    scale.events.streams.postgres --> scale.server.extensions.EventsExtension.register { PgEventStream }
    scale.events.streams.postgres --> scale.tests.data.test_pg_stream { PgEventStream, _STREAM_SCHEMA }
    scale.events.streams.postgres --> scale.tests.misc.test_events { PgEventStream }
    scale.injector.binary --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._build_client_bundle { host_toolchain_path }
    scale.injector.binary --> scale.deploy.target.kubernetes.runtime_bootstrap.build_bootstrap_init_container { OFFICIAL_IMAGE }
    scale.injector.binary --> scale.deploy.target.kubernetes.runtime_bootstrap.image_pull_policy { OFFICIAL_IMAGE }
    scale.injector.binary --> scale.deploy.target.kubernetes.target.KubernetesTarget.deploy { deploy_generation_refusal, node_arch, preflight_pod_runtime }
    scale.injector.binary --> scale.deploy.target.kubernetes.target.KubernetesTarget.generate_manifests { resolve_pod_base_image }
    scale.injector.binary --> scale.injector.binary_injector { download_release_binary, host_seal_platform, node_arch, pack_binary_bytes, resolve_console_version, resolve_deploy_version, stage_admin_dist, toolchain_object_key }
    scale.injector.binary --> scale.runtime.realizer.kubernetes_realizer.KubernetesRealizer._deploy_on_pinned_jac { host_toolchain_path }
    scale.injector.binary --> scale.runtime.realizer.kubernetes_realizer.KubernetesRealizer.realize { deploy_generation_refusal, reset_deploy_version_cache }
    scale.injector.binary --> scale.sdk.client.ScaleClient.deploy { reset_deploy_version_cache }
    scale.injector.binary as binary_mod --> scale.tests.deploy.test_client_build_fail_fast;
    scale.injector.binary as binary_mod --> scale.tests.deploy.test_dry_run_purity;
    scale.injector.binary as binary_mod --> scale.tests.deploy.test_memory_trigger_guard;
    scale.injector.binary as binary_mod --> scale.tests.deploy.test_pod_env;
    scale.injector.binary as binary_mod --> scale.tests.deploy.test_version_pin;
    scale.injector.binary --> scale.tests.deploy.test_version_pin { _resolve_target_version }
    scale.injector.binary --> scale.tests.microservices.test_admin_console_source { admin_dist_source, resolve_console_version, resolve_deploy_version, resolve_pinned_version }
    scale.injector.binary as binmod --> scale.tests.microservices.test_binary_cache;
    scale.injector.binary as binary_mod --> scale.tests.microservices.test_binary_injector;
    scale.injector.binary as binary --> scale.tests.microservices.test_binary_injector;
    scale.injector.binary --> scale.tests.microservices.test_binary_injector { cluster_node_archs, download_release_binary, node_arch, pack_binary_bytes, resolve_pod_base_image, stage_admin_dist }
    scale.injector.binary --> scale.tests.microservices.test_seed_determinism { pack_binary_bytes }
    scale.injector.binary_injector --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._build_pod_spec { BinaryInjector }
    scale.injector.binary_injector --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._prepare_injector { select_injector }
    scale.injector.binary_injector as binary_injector_mod --> scale.tests.deploy.test_dry_run_purity;
    scale.injector.binary_injector --> scale.tests.deploy.test_dry_run_purity { BinaryInjector }
    scale.injector.binary_injector as bi_mod --> scale.tests.microservices.test_binary_injector;
    scale.injector.binary_injector --> scale.tests.microservices.test_binary_injector { BinaryInjector }
    scale.injector.bundle --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._build_client_bundle { _stage_app, release_binary_env, remove_stage_root, source_filter_for }
    scale.injector.bundle --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._build_pod_spec { APP_MOUNT_PATH }
    scale.injector.bundle --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._bundle_files { resolve_fleet_entries }
    scale.injector.bundle --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._check_pod_config_resolves { nested_sanitized_tomls, source_filter_for, unresolved_toml_references }
    scale.injector.bundle --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._pod_entrypoint { APP_MOUNT_PATH }
    scale.injector.bundle --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._project_config { _project_config }
    scale.injector.bundle --> scale.deploy.target.kubernetes.runtime_bootstrap { APP_MOUNT_PATH, APP_VOLUME_NAME, JAC_HOME, TOOLCHAIN_SUBDIR }
    scale.injector.bundle --> scale.injector.binary { TOOLCHAIN_SUBDIR }
    scale.injector.bundle --> scale.injector.binary_injector { bundle_object_key, content_address }
    scale.injector.bundle --> scale.injector.pvc_injector { APP_MOUNT_PATH, APP_VOLUME_NAME, bundle_object_key, content_address, ensure_jac_toml_cmd, pack_jab }
    scale.injector.bundle --> scale.runtime.realizer.kubernetes_realizer.KubernetesRealizer._deploy_on_pinned_jac { release_binary_env }
    scale.injector.bundle --> scale.tests.deploy.test_client_build_fail_fast { release_binary_env }
    scale.injector.bundle --> scale.tests.deploy.test_client_build_stage { bundle_source_files, source_filter_for }
    scale.injector.bundle --> scale.tests.deploy.test_pod_env._entrypoint_run { APP_MOUNT_PATH }
    scale.injector.bundle --> scale.tests.microservices.test_app_precompile { DEFAULT_SEAL_TIMEOUT_S, PLACEHOLDER_JAC_TOML, _stage_app, nested_sanitized_tomls, pack_jab, reap_stale_stage_roots, seal_step_env, seal_timeout_setting, stage_roots_in_use }
    scale.injector.bundle --> scale.tests.microservices.test_binary_injector { TOOLCHAIN_SUBDIR }
    scale.injector.bundle --> scale.tests.microservices.test_bundle_jacignore { _stage_app, add_source_members, bundle_source_files, content_address, nested_sanitized_tomls, pack_jab, partition_bundle_sources }
    scale.injector.bundle as bundle --> scale.tests.microservices.test_fat_bundle;
    scale.injector.bundle --> scale.tests.microservices.test_fat_bundle { _strip_external_record_lines, content_address, fat_bundle_enabled, fat_bundle_setting, pack_jab, staged_venv_files }
    scale.injector.bundle --> scale.tests.microservices.test_pvc_injector { pack_jab }
    scale.injector.bundle --> scale.tests.microservices.test_seed_determinism { content_address, pack_jab }
    scale.injector.injector --> scale.injector.pvc_injector { Injector }
    scale.injector.pvc_injector --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._build_pod_spec { VOLUME_PERMS_NAME, build_volume_perms_init_container, runtime_pod_security_context }
    scale.injector.pvc_injector --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._prepare_injector { PvcInjector }
    scale.injector.pvc_injector --> scale.deploy.target.kubernetes.runtime_bootstrap { BUNDLE_MOUNT_PATH, BUNDLE_VOLUME_NAME }
    scale.injector.pvc_injector --> scale.deploy.target.kubernetes.target { bundle_keys_from_pod_spec, bundle_pvc_name }
    scale.injector.pvc_injector --> scale.injector.binary_injector { PvcInjector, bundle_pvc_path }
    scale.injector.pvc_injector --> scale.tests.deploy.test_destroy_reclaim { bundle_pvc_name }
    scale.injector.pvc_injector --> scale.tests.deploy.test_pod_env { RUNTIME_GID, RUNTIME_UID, VOLUME_PERMS_NAME }
    scale.injector.pvc_injector --> scale.tests.microservices.test_binary_injector { BUNDLE_MOUNT_PATH, BUNDLE_VOLUME_NAME }
    scale.injector.pvc_injector --> scale.tests.microservices.test_pvc_injector { BUNDLE_MOUNT_PATH, PvcInjector, RUNTIME_GID, RUNTIME_UID, build_bundle_pvc, build_loader_pod, build_pvc_init_container, bundle_keys_from_pod_spec }
    scale.injector.binary --> scale.injector.binary_injector { read_local_binary }
    scale.injector.binary --> scale.tests.microservices.test_binary_injector { read_local_binary }
    scale.injector.pvc_injector --> scale.tests.deploy.test_pod_env { BUNDLE_MOUNT_PATH, PVC_BOOTSTRAP_NAME, bundle_keys_from_pod_spec }
    scale.injector.pvc_injector --> scale.tests.microservices.test_pvc_injector { pvc_unpack_script }
    scale.memory.context --> scale.runtime.provider.JacScaleRuntime.create_j_context { JScaleExecutionContext }
    scale.models.deploy_context --> scale.deploy.target.kubernetes.database_provisioner { DeployContext }
    scale.models.deploy_context --> scale.deploy.target.kubernetes.kubernetes_target { DATABASE_URL_ENV }
    scale.models.deploy_context --> scale.deploy.target.kubernetes.manifest_builder { DATABASE_URL_ENV, DeployContext }
    scale.models.deploy_context --> scale.deploy.target.kubernetes.target { DeployContext }
    scale.models.deployment_result --> scale.deploy.target.deployment_target { DeploymentResult }
    scale.models.deployment_result --> scale.deploy.target.kubernetes.target { DeploymentResult }
    scale.models.deployment_result --> scale.sdk { DeploymentResult }
    scale.models.deployment_result --> scale.sdk.client { DeploymentResult }
    scale.models.deployment_result --> scale.tests.deploy.test_deploy_k8s { DeploymentResult }
    scale.models.progress --> scale.deploy.target.kubernetes.kubernetes_target { EventSink, NoopSink, ProgressEvent }
    scale.models.progress --> scale.sdk { CallbackSink, EventSink, ProgressEvent }
    scale.models.progress --> scale.sdk.client { CallbackSink, EventSink, NoopSink, ProgressEvent }
    scale.models.progress --> scale.sdk.events { EventSink, ProgressEvent }
    scale.models.resource_status --> scale.admin.deploy_health { assess_workload }
    scale.models.resource_status --> scale.deploy.autoscale.autoscaler { ResourceStatus, ResourceStatusInfo, assess_workload, field_of }
    scale.models.resource_status --> scale.deploy.autoscale.hpa_autoscaler { ResourceStatus }
    scale.models.resource_status --> scale.deploy.autoscale.keda_autoscaler { ResourceStatus }
    scale.models.resource_status --> scale.deploy.target.deployment_target { ResourceStatusInfo }
    scale.models.resource_status --> scale.deploy.target.kubernetes.kubernetes_target { ResourceStatus, ResourceStatusInfo, assess_workload }
    scale.models.resource_status --> scale.deploy.target.kubernetes.manifest_builder { REPLICA_FLOOR_ANNOTATION }
    scale.models.resource_status --> scale.deploy.target.kubernetes.target { ResourceStatus, assess_workload }
    scale.models.resource_status --> scale.sdk { ResourceStatus, ResourceStatusInfo }
    scale.models.resource_status --> scale.sdk.client { ResourceStatusInfo }
    scale.models.resource_status --> scale.tests.deploy.test_deploy_k8s { ResourceStatus }
    scale.models.resource_status --> scale.tests.deploy.test_http_activation_microservices { REPLICA_FLOOR_ANNOTATION, ResourceStatus }
    scale.models.resource_status --> scale.tests.deploy.test_ops_deploy { REPLICA_FLOOR_ANNOTATION }
    scale.models.resource_status --> scale.tests.deploy.test_superseded_deployment_reap { REPLICA_FLOOR_ANNOTATION, assess_workload }
    scale.models.resource_status --> scale.tests.microservices.test_fleet_rollout { REPLICA_FLOOR_ANNOTATION }
    scale.observability.factory --> scale.plugin { UtilityFactory }
    scale.observability.factory --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.setup { UtilityFactory }
    scale.observability.factory --> scale.runtime.realizer.kubernetes_realizer { UtilityFactory }
    scale.observability.factory --> scale.sdk.client.ScaleClient._pick_logger { UtilityFactory }
    scale.observability.factory --> scale.server.extensions.MetricsExtension.register { UtilityFactory }
    scale.observability.factory --> scale.tests.deploy.test_deploy_k8s { UtilityFactory }
    scale.observability.factory --> scale.tests.deploy.test_factories { UtilityFactory }
    scale.observability.factory --> scale.tests.misc.test_metrics { UtilityFactory }
    scale.observability.factory --> scale.tests.misc.test_optional_deps { UtilityFactory }
    scale.observability.logger --> scale.deploy.autoscale.factory { Logger }
    scale.observability.logger --> scale.deploy.autoscale.hpa_autoscaler { Logger }
    scale.observability.logger --> scale.deploy.autoscale.keda_autoscaler { Logger }
    scale.observability.logger --> scale.deploy.target.deployment_target { Logger }
    scale.observability.logger --> scale.deploy.target.factory { Logger }
    scale.observability.logger --> scale.deploy.target.kubernetes.cluster_provider { Logger }
    scale.observability.logger --> scale.deploy.target.kubernetes.ingress { Logger }
    scale.observability.logger --> scale.deploy.target.kubernetes.kubernetes_target { Logger }
    scale.observability.logger --> scale.deploy.target.kubernetes.monitoring { Logger }
    type scale.observability.logger --> scale.deploy.target.registry { Logger }
    scale.observability.logger --> scale.observability.factory { Logger }
    scale.observability.logger --> scale.observability.standard_logger { Logger }
    scale.observability.logger --> scale.sdk.client { Logger }
    scale.observability.logger --> scale.sdk.events { Logger }
    scale.observability.metrics --> scale.admin.admin_portal { MetricsCollector }
    scale.observability.metrics --> scale.observability.factory { MetricsCollector, NoOpMetricsCollector }
    scale.observability.metrics --> scale.observability.prometheus_metrics { MetricsCollector }
    scale.observability.metrics --> scale.server.extensions { MetricsCollector }
    scale.observability.metrics --> scale.tests.misc.test_metrics { NoOpMetricsCollector }
    scale.observability.metrics --> scale.tests.misc.test_optional_deps { NoOpMetricsCollector }
    scale.observability.prometheus_client --> scale.admin.workloads { query as prom_query, query_range as prom_query_range, resolve_prometheus_url, scalar as prom_scalar }
    scale.observability.prometheus_metrics --> scale.observability.factory.UtilityFactory.create_metrics { PrometheusMetricsCollector }
    scale.observability.prometheus_metrics --> scale.tests.misc.test_metrics { PrometheusMetricsCollector }
    scale.observability.prometheus_metrics --> scale.tests.misc.test_optional_deps { PrometheusMetricsCollector }
    scale.observability.standard_logger --> scale.observability.factory.UtilityFactory.create_logger { StandardLogger }
    scale.observability.standard_logger --> scale.tests.deploy.test_http_activation_microservices { StandardLogger }
    scale.runtime.fleet --> scale.admin.logs._fleet_names { fleet_member_names }
    scale.runtime.fleet --> scale.admin.traces._trace_services { fleet_member_names }
    scale.runtime.fleet --> scale.deploy.target.kubernetes.manifest_builder { FleetSpec, fleet_from_config, solo_fleet }
    scale.runtime.fleet --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._build_env { FLEET_ENV }
    scale.runtime.fleet --> scale.deploy.target.kubernetes.target { FleetSpec }
    scale.runtime.fleet --> scale.injector.bundle { FleetSpec }
    scale.runtime.fleet --> scale.plugin._print_local_fleet_banner { format_fleet_lines }
    scale.runtime.fleet --> scale.plugin.scale_cmd { fleet_from_config, fleet_from_env }
    scale.runtime.fleet --> scale.plugin.scale_local_serve { fleet_from_plans }
    scale.runtime.fleet --> scale.runtime.cli.plan { FleetSpec }
    scale.runtime.fleet --> scale.runtime.orchestrator.orchestrator { FleetSpec, ROOT_PREFIX }
    scale.runtime.fleet --> scale.runtime.provider.JacScaleRuntime.get_sv_service_routes { fleet_from_env }
    scale.runtime.fleet --> scale.runtime.realizer.kubernetes_realizer { FleetSpec, fleet_from_config, format_fleet_lines }
    scale.runtime.fleet --> scale.runtime.realizer.local_realizer { FleetSpec }
    scale.runtime.fleet --> scale.tests.apps.test_app_scale_overrides { fleet_from_config }
    scale.runtime.fleet --> scale.tests.apps.test_fleet_from_apps { FLEET_ENV, FleetSpec, ROOT_PREFIX, _compiled_app_edges, consumer_provider_edges, fleet_from_config, fleet_from_env, fleet_of, guard_fleet_routes, order_by_edges, solo_fleet }
    scale.runtime.fleet --> scale.tests.deploy.test_access_hint { fleet_of }
    scale.runtime.fleet --> scale.tests.deploy.test_client_build_stage { FleetMember, FleetSpec }
    scale.runtime.fleet --> scale.tests.deploy.test_deploy_banner { fleet_of }
    scale.runtime.fleet --> scale.tests.deploy.test_deployment_overlay { fleet_of }
    scale.runtime.fleet --> scale.tests.deploy.test_dry_run_purity { fleet_of }
    scale.runtime.fleet --> scale.tests.deploy.test_http_activation_microservices { fleet_of }
    scale.runtime.fleet --> scale.tests.deploy.test_memory_trigger_guard { fleet_of }
    scale.runtime.fleet --> scale.tests.deploy.test_pdb_budget { fleet_of }
    scale.runtime.fleet --> scale.tests.deploy.test_pod_env { FLEET_ENV, fleet_of }
    scale.runtime.fleet --> scale.tests.deploy.test_show_yaml_autoscalers { fleet_of }
    scale.runtime.fleet --> scale.tests.microservices.test_app_precompile { fleet_from_config }
    scale.runtime.provider --> cli.commands.execution.serve { mark_scale_runtime }
    scale.runtime.provider --> runtime.runtime._scale_provider { JacScaleRuntime }
    scale.runtime.provider --> runtime.source_app.main { mark_scale_runtime }
    scale.runtime.provider --> scale.plugin { mark_scale_runtime }
    scale.runtime.provider --> scale.runtime.orchestrator.orchestrator._populate_k8s_urls { JacScaleRuntime }
    scale.runtime.provider --> scale.runtime.rpc.rpc._resolve_call_target { JacScaleRuntime }
    scale.runtime.provider --> scale.server.inprocess.prepare_inprocess_runtime { mark_scale_runtime }
    scale.runtime.provider as provider_mod --> scale.tests.server.test_sv_auth_forward;
    scale.runtime.provider --> scale.tests.server.test_sv_auth_forward { JacScaleRuntime }
    scale.runtime.provider --> scale.tests.server.test_sv_streaming { JacScaleRuntime }
    scale.runtime.routing --> scale.admin.admin_portal._classify_path { GATEWAY_WELLKNOWN_SEGMENTS }
    scale.runtime.routing --> scale.runtime.fleet { guard_route_prefix }
    scale.runtime.routing --> scale.runtime.gateway.dispatch { GATEWAY_API_SEGMENTS, GATEWAY_LISTING_SEGMENTS, GATEWAY_PAGE_SEGMENTS, GATEWAY_WELLKNOWN_SEGMENTS }
    scale.runtime.routing --> scale.runtime.gateway.microservice_gateway { GATEWAY_BARE_API_PATHS, GATEWAY_BUILTIN_PREFIXES, GATEWAY_DISCOVERY_SEGMENTS, GATEWAY_REPLICATED_SEGMENTS }
    scale.runtime.routing --> scale.runtime.gateway.route_table.ServiceRouteTable.learn { is_learnable_prefix }
    scale.runtime.routing --> scale.tests.microservices.test_routing_guard { GATEWAY_API_SEGMENTS, GATEWAY_BUILTIN_PREFIXES, GATEWAY_CLIENT_SEGMENT, GATEWAY_DISCOVERY_SEGMENTS, GATEWAY_LISTING_SEGMENTS, GATEWAY_REPLICATED_SEGMENTS, GATEWAY_SERVICE_OWNED_SEGMENTS, GATEWAY_WELLKNOWN_SEGMENTS, guard_route_prefix, is_gateway_owned_segment, is_learnable_prefix }
    scale.runtime.cli._narrow --> scale.runtime.cli.diagnostics { bget, dget, effective_resources, iget, lget, pod_spec, sget }
    scale.runtime.cli._narrow --> scale.runtime.cli.plan { dget, fget, iget, lget, pod_spec, sget }
    scale.runtime.cli.diagnostics --> scale.runtime.cli.plan { Diagnostic, PlanValidator, has_errors }
    scale.runtime.cli.diagnostics --> scale.runtime.realizer.kubernetes_realizer.KubernetesRealizer.realize { has_errors }
    scale.runtime.cli.diagnostics --> scale.tests.deploy.test_pdb_budget { PlanValidator }
    scale.runtime.cli.plan --> scale.runtime.realizer.kubernetes_realizer.KubernetesRealizer.realize { print_plan }
    scale.runtime.context.auth_ctx --> scale.runtime.rpc.rpc._rpc_headers { get_current_auth }
    scale.runtime.context.auth_ctx --> scale.server.extensions.ObservabilityExtension.register { reset_current_auth, set_current_auth }
    scale.runtime.context.auth_ctx --> scale.tests.server.test_sv_auth_forward { get_current_auth, reset_current_auth, set_current_auth }
    scale.runtime.context.errors --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.deliver_once { not_found }
    scale.runtime.context.errors --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.forward_root_path { service_unavailable }
    scale.runtime.context.errors --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.forward_to { gateway_timeout, service_unavailable }
    scale.runtime.context.errors --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.forward_to_root { service_unavailable }
    scale.runtime.context.errors --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.handle_builtin_passthrough { not_found }
    scale.runtime.context.errors --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.handle_metrics { error_response }
    scale.runtime.context.errors --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.probe_services { not_found, service_unavailable }
    scale.runtime.context.errors --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.setup.dispatcher { not_found }
    scale.runtime.context.errors --> scale.runtime.middleware.rate_limit.build_rate_limit_middleware { error_response }
    scale.runtime.context.log_emit --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.setup { install_structured_logging }
    scale.runtime.context.log_emit --> scale.server.extensions.ObservabilityExtension.register { install_structured_logging }
    scale.runtime.context.log_emit --> scale.tests.misc.test_log_emit { _JacJsonFormatter, emit_log_record, install_structured_logging }
    scale.runtime.context.service_routing --> scale.config.plugin_config { KEDA_INTERCEPTOR_SERVICE_ADDRESS }
    scale.runtime.context.service_routing --> scale.deploy.autoscale.factory.AutoscalerFactory.create { resolve_interceptor_service_address }
    scale.runtime.context.service_routing --> scale.deploy.autoscale.http_activation_config.build_http_activation_spec { k8s_service_dns_host }
    scale.runtime.context.service_routing --> scale.deploy.autoscale.keda_autoscaler { KEDA_INTERCEPTOR_SERVICE_ADDRESS }
    scale.runtime.context.service_routing --> scale.deploy.target.kubernetes.manifest_builder { resolve_http_activation_config }
    scale.runtime.context.service_routing --> scale.deploy.target.kubernetes.runtime_resolver { ServiceRoute, resolve_service_route }
    scale.runtime.context.service_routing --> scale.deploy.target.kubernetes.target { resolve_interceptor_service_address }
    scale.runtime.context.service_routing --> scale.tests.deploy.test_service_routing { KEDA_INTERCEPTOR_SERVICE_ADDRESS, ServiceRoute, k8s_service_dns_host, resolve_http_activation_config, resolve_interceptor_service_address, resolve_service_route }
    scale.runtime.context.service_routing --> scale.tests.server.test_sv_auth_forward { ServiceRoute }
    scale.runtime.context.trace_ctx --> scale.runtime.context.errors.error_response { get_current_trace }
    scale.runtime.context.trace_ctx --> scale.runtime.context.log_emit.install_structured_logging { install_trace_log_filter }
    scale.runtime.context.trace_ctx --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.build_forward_headers { ensure_trace_id, get_current_trace }
    scale.runtime.context.trace_ctx --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.setup { ensure_trace_id, reset_current_trace, set_current_trace }
    scale.runtime.context.trace_ctx --> scale.runtime.rpc.rpc._rpc_headers { get_current_trace }
    scale.runtime.context.trace_ctx --> scale.server.extensions.ObservabilityExtension.register { ensure_trace_id, reset_current_trace, set_current_trace }
    scale.runtime.context.trace_ctx --> scale.tests.misc.test_log_emit { TraceIdLogFilter, install_trace_log_filter, reset_current_trace, set_current_trace }
    scale.runtime.context.trace_ctx --> scale.tests.server.test_sv_auth_forward { ensure_trace_id, get_current_trace, reset_current_trace, set_current_trace }
    scale.runtime.context.tracing --> scale.admin.ops { tracing_active }
    scale.runtime.context.tracing --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.build_forward_headers { current_traceparent }
    scale.runtime.context.tracing --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.setup { end_span, install_tracing, start_server_span }
    scale.runtime.context.tracing --> scale.runtime.rpc.rpc._rpc_headers { current_traceparent }
    scale.runtime.context.tracing --> scale.server.extensions.ObservabilityExtension.register { end_span, install_tracing, start_server_span, tracing_installed }
    scale.runtime.context.tracing --> scale.tests.misc.test_tracing { build_traceparent, current_traceparent, end_memory_span, end_span, install_tracing, new_span_id, parse_traceparent, start_memory_span, start_server_span, trace_id_hex, tracing_active, uuid_to_trace_id }
    scale.runtime.context.util --> scale.admin.k8s_ops { in_cluster_namespace }
    scale.runtime.context.util --> scale.deploy.target.kubernetes.database_provisioner { k8s_safe_name }
    scale.runtime.context.util --> scale.deploy.target.kubernetes.manifest_builder { GATEWAY_NAME, k8s_safe_name }
    scale.runtime.context.util --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._build_client_bundle { jac_executable }
    scale.runtime.context.util --> scale.deploy.target.kubernetes.manifest_builder.ManifestBuilder._peer_dns_url { k8s_service_dns_url }
    scale.runtime.context.util --> scale.deploy.target.kubernetes.runtime_resolver { DEFAULT_GATEWAY_PORT }
    scale.runtime.context.util --> scale.deploy.target.kubernetes.runtime_resolver.build_k8s_registry_routes { in_cluster_namespace }
    scale.runtime.context.util --> scale.deploy.target.kubernetes.target { GATEWAY_NAME, k8s_safe_name }
    scale.runtime.context.util --> scale.runtime.cli.diagnostics { GATEWAY_NAME }
    scale.runtime.context.util --> scale.runtime.cli.plan { GATEWAY_NAME }
    scale.runtime.context.util --> scale.runtime.context.service_routing { k8s_safe_name, k8s_service_dns_host }
    scale.runtime.context.util --> scale.runtime.gateway.embedded_gateway { DEFAULT_CLIENT_DIST_DIR, DEFAULT_GATEWAY_HOST, DEFAULT_GATEWAY_PORT }
    scale.runtime.context.util --> scale.runtime.gateway.microservice_gateway { DEFAULT_CLIENT_DIST_DIR, DEFAULT_GATEWAY_HOST, DEFAULT_GATEWAY_PORT }
    scale.runtime.context.util --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.aggregate_graph_data { http_forward_timeout }
    scale.runtime.context.util --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.forward_to { http_forward_timeout }
    scale.runtime.context.util --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.probe_services { http_forward_timeout }
    scale.runtime.context.util --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.refresh_app_routes { route_refresh_seconds }
    scale.runtime.context.util --> scale.runtime.gateway.process_gateway { DEFAULT_CLIENT_DIST_DIR, DEFAULT_GATEWAY_HOST, DEFAULT_GATEWAY_PORT }
    scale.runtime.context.util --> scale.runtime.orchestrator.orchestrator { DEFAULT_GATEWAY_HOST, DEFAULT_GATEWAY_PORT }
    scale.runtime.context.util --> scale.runtime.orchestrator.process_manager.ServiceProcessManager._assign_free_port { pick_free_port }
    scale.runtime.context.util --> scale.runtime.orchestrator.process_manager.ServiceProcessManager._assign_port { pick_free_port }
    scale.runtime.context.util --> scale.runtime.orchestrator.process_manager.ServiceProcessManager._await_lead { wait_for_health }
    scale.runtime.context.util --> scale.runtime.orchestrator.process_manager.ServiceProcessManager.start_service { jac_executable }
    scale.runtime.context.util --> scale.sdk.client { k8s_safe_name }
    scale.runtime.context.util --> scale.tests.apps.test_app_scale_overrides { boot_health_timeout, http_forward_timeout }
    scale.runtime.context.util --> scale.tests.deploy.test_client_build_deps { jac_executable }
    scale.runtime.context.util --> scale.tests.deploy.test_client_build_fail_fast { jac_executable }
    scale.runtime.context.util --> scale.tests.deploy.test_client_build_stage { jac_executable }
    scale.runtime.context.util --> scale.tests.deploy.test_dry_run_plan_rate_limit { jac_executable }
    scale.runtime.context.util --> scale.tests.deploy.test_gateway_config_isolation { GATEWAY_NAME, k8s_safe_name }
    scale.runtime.context.util --> scale.tests.deploy.test_http_activation_microservices { GATEWAY_NAME }
    scale.runtime.context.util --> scale.tests.deploy.test_memory_trigger_guard { GATEWAY_NAME }
    scale.runtime.context.util --> scale.tests.deploy.test_pod_env { GATEWAY_NAME }
    scale.runtime.context.util --> scale.tests.microservices.test_gateway { http_forward_timeout }
    scale.runtime.context.util --> scale.tests.microservices.test_k8s_health_probe { jac_executable }
    scale.runtime.context.util --> scale.tests.server.test_acl_field_write._prewarm { jac_executable }
    scale.runtime.context.util --> scale.tests.server.test_admin { jac_executable }
    scale.runtime.context.util --> scale.tests.server.test_app_tokens._prewarm { jac_executable }
    scale.runtime.context.util --> scale.tests.server.test_examples.JacScaleTestRunner.start_server { jac_executable }
    scale.runtime.context.util --> scale.tests.server.test_metrics_workers { jac_executable }
    scale.runtime.context.util --> scale.tests.server.test_metrics_workers._serve_exported { jac_executable }
    scale.runtime.context.util --> scale.tests.server.test_root_bind_fail_closed._prewarm { jac_executable }
    scale.runtime.context.util --> scale.tests.server.test_serve { jac_executable }
    scale.runtime.context.util --> scale.tests.support.start_server { jac_executable }
    scale.runtime.context.errors --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.forward_to { bad_gateway }
    scale.runtime.context.errors --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.probe_services { gateway_timeout }
    scale.runtime.context.service_routing --> scale.runtime.context.util.http_forward_timeout { HTTP_ACTIVATED_WAKE_TIMEOUT, is_http_activated }
    scale.runtime.context.service_routing --> scale.runtime.rpc.rpc._sv_rpc_timeout { HTTP_ACTIVATED_WAKE_TIMEOUT, is_http_activated }
    scale.runtime.gateway.dispatch --> scale.runtime.gateway.embedded_gateway { ROUTE_PROXY, ROUTE_STATIC, classify_route }
    scale.runtime.gateway.dispatch --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.setup.dispatcher { ROUTE_ADMIN, ROUTE_BUILTIN, ROUTE_CLIENT_PAGE, ROUTE_IDENTITY, ROUTE_PROXY, classify_route }
    scale.runtime.gateway.dispatch --> scale.tests.apps.test_fleet_from_apps { ROUTE_PROXY, classify_route }
    scale.runtime.gateway.dispatch --> scale.tests.microservices.test_dispatch { ROUTE_ADMIN, ROUTE_PROXY, ROUTE_STATIC, classify_route }
    scale.runtime.gateway.dispatch --> scale.tests.microservices.test_gateway_docs_precedence { ROUTE_BUILTIN, ROUTE_CLIENT_PAGE, classify_route }
    scale.runtime.gateway.embedded_gateway --> scale.tests.microservices.test_embedded_gateway { EmbeddedGateway }
    scale.runtime.gateway.gateway --> scale.runtime.gateway.embedded_gateway { Gateway }
    scale.runtime.gateway.gateway --> scale.runtime.gateway.process_gateway { Gateway }
    scale.runtime.gateway.microservice_gateway --> scale.runtime.gateway.process_gateway { MicroserviceGateway }
    scale.runtime.gateway.microservice_gateway --> scale.tests.apps.test_fleet_from_apps { MicroserviceGateway }
    scale.runtime.gateway.microservice_gateway --> scale.tests.microservices.test_app_routes { MicroserviceGateway }
    scale.runtime.gateway.microservice_gateway --> scale.tests.microservices.test_gateway { MicroserviceGateway }
    scale.runtime.gateway.microservice_gateway --> scale.tests.microservices.test_gateway_docs_precedence { MicroserviceGateway }
    scale.runtime.gateway.microservice_gateway --> scale.tests.microservices.test_gateway_webapp { MicroserviceGateway }
    scale.runtime.gateway.microservice_gateway --> scale.tests.microservices.test_k8s_health_probe { MicroserviceGateway }
    scale.runtime.gateway.microservice_gateway --> scale.tests.server.test_static_fallback { MicroserviceGateway }
    scale.runtime.gateway.microservice_gateway --> scale.tests.server.test_stream_ws { MicroserviceGateway }
    scale.runtime.gateway.openapi_agg --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.handle_openapi { aggregate_openapi }
    scale.runtime.gateway.openapi_agg --> scale.runtime.gateway.route_table.learn_service_routes { SpecFetch, fetch_service_spec }
    scale.runtime.gateway.openapi_agg --> scale.tests.microservices.test_gateway { _prefixed_paths }
    scale.runtime.gateway.openapi_agg --> scale.tests.microservices.test_openapi_agg { _agg_logger, aggregate_openapi }
    scale.runtime.gateway.process_gateway --> scale.runtime.orchestrator.orchestrator { ProcessGateway }
    scale.runtime.gateway.route_table --> scale.runtime.gateway.microservice_gateway { ServiceRouteTable }
    scale.runtime.gateway.route_table --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.refresh_app_routes { learn_service_routes }
    scale.runtime.gateway.route_table --> scale.tests.microservices.test_app_routes { ServiceRouteTable, literal_prefix }
    scale.runtime.gateway.route_table --> scale.tests.microservices.test_gateway.gw_route_table_for_poison_test { ServiceRouteTable }
    scale.runtime.gateway.route_table --> scale.tests.microservices.test_route_learning { ServiceRouteTable }
    scale.runtime.gateway.service_registry --> scale.deploy.target.kubernetes.runtime_resolver { ServiceEntry, ServiceRegistry }
    scale.runtime.gateway.service_registry --> scale.runtime.gateway.embedded_gateway { ServiceRegistry }
    scale.runtime.gateway.service_registry --> scale.runtime.gateway.microservice_gateway { ServiceEntry, ServiceRegistry, ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.runtime.gateway.microservice_gateway._install_ws_catchall { ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.runtime.gateway.openapi_agg { ServiceEntry, ServiceRegistry }
    scale.runtime.gateway.service_registry --> scale.runtime.gateway.process_gateway { ServiceRegistry }
    scale.runtime.gateway.service_registry --> scale.runtime.gateway.route_table { ServiceEntry, ServiceRegistry, ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.runtime.orchestrator.local_deployer { ServiceEntry, ServiceRegistry, ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.runtime.orchestrator.orchestrator { ServiceEntry, ServiceRegistry, ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.runtime.orchestrator.process_manager { ServiceEntry, ServiceRegistry, ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.tests.apps.test_fleet_from_apps { ServiceEntry, ServiceRegistry, ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.tests.deploy.test_deployer { ServiceEntry, ServiceRegistry, ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.tests.deploy.test_pod_env { ServiceEntry, ServiceRegistry }
    scale.runtime.gateway.service_registry --> scale.tests.microservices.test_app_routes { ServiceEntry, ServiceRegistry, ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.tests.microservices.test_boot_grace { ServiceEntry, ServiceRegistry, ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.tests.microservices.test_boot_order { ServiceEntry, ServiceRegistry, ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.tests.microservices.test_embedded_gateway { ServiceEntry, ServiceRegistry }
    scale.runtime.gateway.service_registry --> scale.tests.microservices.test_gateway { ServiceEntry, ServiceRegistry, ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.tests.microservices.test_gateway_docs_precedence { ServiceRegistry }
    scale.runtime.gateway.service_registry --> scale.tests.microservices.test_gateway_webapp { ServiceEntry, ServiceRegistry, ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.tests.microservices.test_k8s_health_probe { ServiceEntry, ServiceRegistry, ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.tests.microservices.test_microservices_registry { ServiceEntry, ServiceRegistry, ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.tests.microservices.test_openapi_agg { ServiceEntry, ServiceRegistry, ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.tests.microservices.test_route_learning { ServiceEntry, ServiceStatus }
    scale.runtime.gateway.service_registry --> scale.tests.microservices.test_stop_signal_scope { ServiceEntry, ServiceRegistry }
    scale.runtime.gateway.service_registry --> scale.tests.server.test_static_fallback { ServiceRegistry }
    scale.runtime.gateway.service_registry --> scale.tests.server.test_stream_ws { ServiceEntry, ServiceRegistry, ServiceStatus }
    scale.runtime.middleware.metrics --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.handle_metrics { render_metrics }
    scale.runtime.middleware.metrics --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.setup { build_gateway_metrics }
    scale.runtime.middleware.metrics --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.setup.dispatcher { classify_outcome }
    scale.runtime.middleware.metrics --> scale.tests.microservices.test_gateway { build_gateway_metrics, classify_outcome }
    scale.runtime.middleware.middleware --> scale.runtime.gateway.gateway { MiddlewareRegistry }
    scale.runtime.middleware.middleware --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.setup { Middleware, MiddlewareRegistry }
    scale.runtime.middleware.middleware --> scale.tests.microservices.test_embedded_gateway { Middleware }
    scale.runtime.middleware.middleware --> scale.tests.microservices.test_middleware { Middleware, MiddlewareRegistry }
    scale.runtime.middleware.rate_limit --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.setup { build_rate_limit_middleware }
    scale.runtime.middleware.rate_limit --> scale.tests.microservices.test_rate_limit { InProcessRateLimiter, build_rate_limit_middleware }
    scale.runtime.middleware.ws_forward --> scale.runtime.gateway.microservice_gateway._install_ws_catchall { websocket_forward }
    scale.runtime.middleware.ws_forward --> scale.tests.server.test_stream_ws { _select_handshake_headers, _to_ws_scheme, websocket_forward }
    scale.runtime.orchestrator.local_deployer --> scale.plugin.scale_cmd { LocalDeployer }
    scale.runtime.orchestrator.local_deployer --> scale.runtime.orchestrator.orchestrator { LocalDeployer }
    scale.runtime.orchestrator.local_deployer --> scale.tests.deploy.test_deployer { LocalDeployer }
    scale.runtime.orchestrator.orchestrator --> scale.plugin.scale_cmd { ServiceRegistry, build_registry, start_gateway_only }
    scale.runtime.orchestrator.orchestrator --> scale.runtime.realizer.local_realizer { start_fleet_mode }
    scale.runtime.orchestrator.orchestrator --> scale.tests.apps.test_fleet_from_apps { build_registry }
    scale.runtime.orchestrator.process_manager --> scale.runtime.orchestrator.local_deployer { ServiceProcessManager }
    scale.runtime.orchestrator.process_manager --> scale.runtime.orchestrator.local_deployer.LocalDeployer.status { _pid_alive, _read_pidfile, _read_portfile }
    scale.runtime.orchestrator.process_manager --> scale.runtime.orchestrator.orchestrator { ServiceProcessManager }
    scale.runtime.orchestrator.process_manager --> scale.tests.microservices.test_boot_grace { ServiceProcessManager }
    scale.runtime.orchestrator.process_manager --> scale.tests.microservices.test_boot_order { ServiceProcessManager }
    scale.runtime.orchestrator.process_manager --> scale.tests.microservices.test_k8s_health_probe { ServiceProcessManager }
    scale.runtime.orchestrator.process_manager --> scale.tests.microservices.test_stop_signal_scope { ServiceProcessManager, _owns_group, _signal_group }
    scale.runtime.planner.planner --> scale.runtime.realizer.local_realizer { TOPOLOGY_MICROSERVICE, plan_realization }
    scale.runtime.planner.planner --> scale.tests.microservices.test_planner { plan_realization }
    scale.runtime.realizer.kubernetes_realizer --> scale.plugin.scale_deploy { KubernetesRealizer }
    scale.runtime.realizer.kubernetes_realizer as realizer_mod --> scale.tests.deploy.test_deploy_banner;
    scale.runtime.realizer.kubernetes_realizer --> scale.tests.deploy.test_deploy_banner { KubernetesRealizer }
    scale.runtime.realizer.kubernetes_realizer as realizer_mod --> scale.tests.deploy.test_dry_run_purity;
    scale.runtime.realizer.kubernetes_realizer --> scale.tests.deploy.test_dry_run_purity { KubernetesRealizer }
    scale.runtime.realizer.kubernetes_realizer --> scale.tests.deploy.test_version_pin { DELEGATED_ENV, KubernetesRealizer, pinned_deploy_argv }
    scale.runtime.realizer.local_realizer --> scale.plugin.scale_local_serve { LocalRealizer }
    scale.runtime.rpc.breaker --> scale.runtime.rpc.rpc { _BREAKER_COOLDOWN_SECONDS, breaker_record_failure, breaker_record_success, breaker_should_skip }
    scale.runtime.rpc.breaker --> scale.tests.server.test_sv_auth_forward { _BREAKER_TRIP_THRESHOLD, _breaker_force_cooldown_elapsed, _breaker_peek, _breaker_reset, breaker_record_failure, breaker_record_success, breaker_should_skip }
    scale.runtime.rpc.rpc --> scale.runtime.transport.transport.HttpTransport.call_function { service_call }
    scale.runtime.rpc.rpc --> scale.runtime.transport.transport.HttpTransport.call_walker { walker_call }
    scale.runtime.rpc.rpc --> scale.tests.apps.test_app_scale_overrides { _sv_rpc_timeout }
    scale.runtime.rpc.rpc as rpc_mod --> scale.tests.server.test_sv_auth_forward;
    scale.runtime.rpc.rpc --> scale.tests.server.test_sv_auth_forward { _RPC_MAX_ATTEMPTS, _sv_rpc_timeout }
    scale.runtime.transport.http_forward --> scale.runtime.gateway.microservice_gateway { raw_forward }
    scale.runtime.transport.http_forward --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.aggregate_graph_data { raw_forward }
    scale.runtime.transport.http_forward --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.forward_to { stream_forward }
    scale.runtime.transport.http_forward --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.probe_services { stream_forward }
    scale.runtime.transport.http_forward --> scale.runtime.gateway.openapi_agg.fetch_service_spec { raw_forward }
    scale.runtime.transport.http_forward --> scale.tests.server.test_stream_ws { ForwardResult, raw_forward, stream_forward }
    scale.runtime.transport.transport --> scale.runtime.gateway.embedded_gateway { ServiceTransport }
    scale.runtime.transport.transport --> scale.runtime.provider.JacScaleRuntime.sv_service_call { http_transport }
    scale.runtime.transport.transport --> scale.runtime.provider.JacScaleRuntime.sv_walker_call { http_transport }
    scale.runtime.transport.transport --> scale.tests.microservices.test_embedded_gateway { InProcessTransport }
    scale.scheduler.fire_executor --> scale.scheduler.scheduler.new_engine { FireTimeExecutor }
    scale.scheduler.scheduler --> scale.server.jobs_ext { JacScaleScheduler, TriggerSpec }
    scale.scheduler.scheduler --> scale.tests.misc.test_optional_deps { JacScaleScheduler, TriggerSpec }
    scale.scheduler.scheduler --> scale.tests.server.test_pg_job_store { PgJobStore }
    scale.scheduler.scheduler --> scale.tests.server.test_scheduler_endpoints { MemoryJobStore, TriggerSpec }
    scale.scheduler.scheduler --> scale.tests.server.test_scheduler_multipod { JOBS_CHANGED_CHANNEL, JacScaleScheduler, PgJobStore, TriggerSpec, new_engine }
    scale.scheduler.scheduler_models --> scale.server.jobs_ext { CreateJobRequest, UpdateJobRequest }
    scale.sdk.client --> scale.sdk { ScaleClient, deploy }
    scale.sdk.events --> scale.sdk | scale.sdk.client { EventLogger }
    scale.sdk.spec --> scale.sdk | scale.sdk.client { DeploySpec }
    scale.server.extensions --> scale.runtime.provider.JacScaleRuntime.get_server_extensions { scale_extensions }
    scale.server.extensions --> scale.tests.data.test_gateway_owned_identity { fleet_provisions_unknown_users }
    scale.server.extensions --> scale.tests.server.test_scheduler_multipod { validate_events_url as _validate_events_url }
    scale.server.inprocess --> client.targets.desktop.native.host_boot.serve_program { prepare_inprocess_runtime }
    scale.server.inprocess --> scale.tests.scale_test_client.ScaleTestClient._initialize { prepare_inprocess_runtime }
    scale.server.inprocess --> scale.tests.server.test_host_serving { prepare_inprocess_runtime }
    scale.server.jobs_ext --> scale.server.extensions { JobsExtension }
    scale.server.jobs_ext --> scale.tests.server.test_scheduler_endpoints { _err_response }
    scale.server.sso_ext --> scale.server.extensions { ApiKeyExtension, SSOExtension }
    scale.server.sso_ext --> scale.tests.server.test_firebase_auth_sso { SSOExtension }
    scale.server.sso_ext --> scale.tests.server.test_sso { SSOExtension, resolve_sso_client_redirect }
    scale.server.webhook_ext --> scale.server.extensions { WebhookExtension }
    scale.server.websocket_ext --> scale.server.extensions { WebSocketExtension }
    scale.server.extensions --> scale.tests.server.test_auth_policy_startup { AdminExtension, MailExtension }
    scale.shared.enums --> scale.sso.sso_auth { Operations, Platforms }
    scale.shared.enums --> scale.tests.server.test_firebase_auth_sso { Operations, Platforms }
    scale.shared.utils --> scale.server.sso_ext { is_safe_loopback_redirect }
    scale.shared.utils --> scale.sso.sso_auth { is_safe_loopback_redirect }
    scale.shared.utils --> scale.tests.server.test_sso { is_safe_loopback_redirect }
    scale.sso.apple --> scale.sso.sso_auth.SSOAuth.get_sso { AppleSSOProvider }
    scale.sso.apple --> scale.tests.server.test_oauth_providers { AppleSSOProvider }
    scale.sso.apple --> scale.tests.server.test_sso { AppleSSOProvider }
    scale.sso.firebase --> scale.sso.sso_auth.SSOAuth.get_sso { FirebaseSSOProvider }
    scale.sso.firebase --> scale.tests.server.test_firebase_auth_sso { FirebaseSSOProvider }
    scale.sso.github --> scale.sso.sso_auth.SSOAuth.get_sso { GithubSSOProvider }
    scale.sso.github --> scale.tests.server.oauth_fixtures { GithubSSOProvider }
    scale.sso.github --> scale.tests.server.test_oauth_providers { GithubSSOProvider }
    scale.sso.github --> scale.tests.server.test_oauth_session { GithubSSOProvider }
    scale.sso.github --> scale.tests.server.test_sso { GithubSSOProvider }
    scale.sso.google --> scale.sso.sso_auth.SSOAuth.get_sso { GoogleSSOProvider }
    scale.sso.google --> scale.tests.server.test_oauth_providers { GoogleSSOProvider }
    scale.sso.google --> scale.tests.server.test_sso { GoogleSSOProvider }
    scale.sso.oauth_session --> scale.server.sso_ext { OAuthSession }
    scale.sso.oauth_session --> scale.sso.sso_auth { OAuthSession, challenge_of, complete_identity }
    scale.sso.oauth_session --> scale.tests.server.test_oauth_session { OAuthSession, challenge_of, complete_identity }
    scale.sso.oauth_session --> scale.tests.server.test_registration_challenge { complete_identity }
    scale.sso.provider --> scale.server.sso_ext { OAuth2CodeProvider }
    scale.sso.provider --> scale.sso.apple { OAuth2CodeProvider, SSOUserInfo, decode_jwt_payload_unverified }
    scale.sso.provider --> scale.sso.firebase { SSOProvider, SSOUserInfo }
    scale.sso.provider --> scale.sso.github { OAuth2CodeProvider, SSOUserInfo }
    scale.sso.provider --> scale.sso.google { OAuth2CodeProvider, SSOUserInfo }
    scale.sso.provider --> scale.sso.oauth_session { OAuth2CodeProvider, SSOUserInfo }
    scale.sso.provider --> scale.sso.sso_auth { OAuth2CodeProvider, SSOProvider, SSOUserInfo }
    scale.sso.provider --> scale.tests.server.test_firebase_auth_sso { SSOUserInfo }
    scale.sso.provider --> scale.tests.server.test_oauth_session { SSOUserInfo }
    scale.sso.provider --> scale.tests.server.test_registration_challenge { SSOUserInfo }
    scale.sso.provider --> scale.tests.server.test_sso { SSOUserInfo }
    scale.sso.sso_auth --> scale.server.sso_ext { SSOAuth }
    scale.sso.sso_auth --> scale.tests.server.test_firebase_auth_sso { SSOAuth }
    scale.sso.sso_auth --> scale.tests.server.test_sso { SSOAuth }
    scale.sso.oauth_session --> scale.sso.sso_auth { OAuthLogin }
    scale.state.factory --> scale.runtime.middleware.rate_limit { get_state_backend }
    scale.state.factory --> scale.tests.microservices.test_rate_limit._reset_state { _backend_holder }
    scale.state.factory as factory_mod --> scale.tests.misc.test_state_backend_selection;
    scale.state.factory --> scale.tests.misc.test_state_backend_selection { get_state_backend, in_fleet }
    scale.state.pg_state_backend --> scale.runtime.provider { PgStateBackend as _state_anchor }
    scale.state.pg_state_backend --> scale.state.factory { PgStateBackend }
    scale.state.state_backend --> scale.runtime.middleware.rate_limit { StateBackend }
    scale.state.state_backend --> scale.state.factory { InProcessStateBackend, StateBackend }
    scale.state.state_backend --> scale.state.pg_state_backend { StateBackend }
    scale.state.state_backend --> scale.tests.misc.test_state_backend_selection { InProcessStateBackend }
    scale.storage.bucket_storage --> scale.storage.gcs_storage { BucketStorage }
    scale.storage.bucket_storage --> scale.storage.s3_storage { BucketStorage }
    scale.storage.factory --> scale.runtime.provider.JacScaleRuntime.store { StorageFactory }
    scale.storage.factory --> scale.tests.data.test_firebase_env { StorageFactory }
    scale.storage.gcs_storage --> scale.storage.factory.StorageFactory.create { GcsStorage }
    scale.storage.gcs_storage --> scale.tests.data.test_gcs_storage { GcsStorage }
    scale.storage.s3_storage --> scale.storage.factory.StorageFactory.create { S3Storage }
    scale.storage.s3_storage --> scale.tests.data.test_s3_storage { S3Storage }
    scale.tests.scale_test_client --> scale.tests.microservices.test_app_routes { ScaleTestClient, make_client }
    scale.tests.scale_test_client --> scale.tests.misc.test_llm_telemetry { ScaleTestClient, extract_data, make_client }
    scale.tests.scale_test_client --> scale.tests.misc.test_metrics { ScaleTestClient }
    scale.tests.scale_test_client --> scale.tests.server.test_admin { ScaleTestClient, extract_data, make_client }
    scale.tests.scale_test_client --> scale.tests.server.test_admin_workloads { extract_data, make_client }
    scale.tests.scale_test_client --> scale.tests.server.test_error_envelope { extract_data, make_client }
    scale.tests.scale_test_client --> scale.tests.server.test_file_upload { ScaleTestClient, extract_data, make_client }
    scale.tests.scale_test_client --> scale.tests.server.test_firebase_auth_sso { extract_data, make_client }
    scale.tests.scale_test_client --> scale.tests.server.test_health_fail_soft { make_client }
    scale.tests.scale_test_client --> scale.tests.server.test_middleware_async_root { ScaleTestClient, extract_data, make_client }
    scale.tests.scale_test_client --> scale.tests.server.test_restspec { ScaleTestClient, extract_data, make_client }
    scale.tests.scale_test_client --> scale.tests.server.test_scheduler_endpoints { ScaleTestClient }
    scale.tests.scale_test_client --> scale.tests.server.test_serve { ScaleTestClient, extract_data, make_client }
    scale.tests.scale_test_client --> scale.tests.server.test_webhook { ScaleTestClient, extract_data, make_client }
    scale.tests.scale_test_client --> scale.tests.server.test_ws_functions { make_client }
    scale.tests.scale_test_client --> scale.tests.server.test_ws_hardening { make_client }
    scale.tests.support --> scale.tests.data.test_async_io_blocking { get_free_port, register_user, start_server }
    scale.tests.support --> scale.tests.deploy.test_client_build_fail_fast { require_pod_binary }
    scale.tests.support --> scale.tests.deploy.test_ops_deploy { RecordingHost }
    scale.tests.support --> scale.tests.deploy.test_ops_health { RecordingHost }
    scale.tests.support --> scale.tests.deploy.test_ops_network { RecordingHost }
    scale.tests.support --> scale.tests.microservices.test_app_precompile { require_pod_binary }
    scale.tests.support --> scale.tests.microservices.test_bundle_jacignore { pod_binary, require_pod_binary }
    scale.tests.support --> scale.tests.microservices.test_fat_bundle { require_pod_binary }
    scale.tests.support --> scale.tests.microservices.test_gateway { get_free_port }
    scale.tests.support --> scale.tests.microservices.test_k8s_health_probe { get_free_port }
    scale.tests.support --> scale.tests.microservices.test_pvc_injector { pod_binary, require_pod_binary }
    scale.tests.support --> scale.tests.microservices.test_seed_determinism { pod_binary, require_pod_binary }
    scale.tests.support --> scale.tests.microservices.test_typed_boundary { get_free_port, start_server, stop_server }
    scale.tests.support --> scale.tests.misc.test_ops_podenv { RecordingHost }
    scale.tests.support --> scale.tests.server.test_acl_field_write { get_free_port, register_user, start_server }
    scale.tests.support --> scale.tests.server.test_admin_logs { RecordingHost }
    scale.tests.support --> scale.tests.server.test_app_tokens { get_free_port, register_user, start_server }
    scale.tests.support --> scale.tests.server.test_examples { get_free_port }
    scale.tests.support --> scale.tests.server.test_firebase_auth_sso { RecordingHost }
    scale.tests.support --> scale.tests.server.test_metrics_workers { cleanup_db_files, get_free_port, start_server, stop_server }
    scale.tests.support --> scale.tests.server.test_root_bind_fail_closed { get_free_port, register_user, start_server }
    scale.tests.support --> scale.tests.server.test_serve { cleanup_db_files, get_free_port, start_server, stop_server }
    scale.tests.support --> scale.tests.server.test_user_identity { extract, get_free_port, register_user, start_server, stop_server }
    scale.tests.toolchain_http --> scale.tests.deploy.test_client_build_fail_fast { mock_downloads }
    scale.tests.toolchain_http --> scale.tests.microservices.test_binary_cache { mock_downloads }
    scale.tests.scale_test_client --> scale.tests.microservices.test_gateway { extract_data, make_client }
    scale.tests.scale_test_client --> scale.tests.server.test_admin { fresh_totp_code, wrong_totp_code }
    scale.tests.scale_test_client --> scale.tests.server.test_serve { fresh_totp_code, totp_code, wrong_totp_code }
    scale.tests.fixture_policy --> scale.tests.scale_test_client { ADMIN_BOOTSTRAP_PASSWORD, apply_fixture_policy }
    scale.tests.fixture_policy --> scale.tests.support { apply_fixture_policy }
    scale.tests.scale_test_client --> scale.tests.server.test_admin { ADMIN_BOOTSTRAP_PASSWORD }
    scale.tests.scale_test_client --> scale.tests.server.test_auth_policy_http { make_client }
    scale.tests.scale_test_client --> scale.tests.server.test_oauth_session { fresh_totp_code }
    scale.tests.deploy.http_activation_test_support --> scale.tests.deploy.test_http_activation_config { default_http_activation_config as _cfg, mocked_keda_autoscaler as _mocked_keda }
    scale.tests.deploy.http_activation_test_support --> scale.tests.deploy.test_http_activation_microservices { default_http_activation_config as _cfg, default_http_activation_spec as _spec, mocked_keda_autoscaler as _mocked_keda }
    scale.tests.server.oauth_fixtures --> scale.tests.server.test_oauth_session { FakeTokens, fake_users, provider }
    scale.tests.server.oauth_fixtures --> scale.tests.server.test_sso { FakeTokens, fake_users }
    scale.utils.vendor_wheels --> scale.injector.bundle._vendor_stage { pod_wheel_target }
    scale.utils.vendor_wheels --> scale.tests.microservices.test_fat_bundle { POD_GLIBC, pod_arch_from_argv, pod_wheel_target }
    scale.webhook.webhook --> scale.server.sso_ext { ApiKeyManager }
    scale.webhook.webhook --> scale.server.webhook_ext { ApiKeyManager, WebhookUtils, rate_window_ok }
    scale.webhook.webhook --> scale.tests.server.test_pg_job_store { ApiKeyManager }
    scale.websocket.backplane --> scale.server.websocket_ext { MemoryBackplane, build_backplane }
    scale.websocket.backplane --> scale.tests.server.test_backplane { PgBackplane }
    scale.websocket.backplane --> scale.tests.server.test_ws_hardening { BaseBackplane, MemoryBackplane, PgBackplane, build_backplane }
    scale.websocket.backplane --> scale.websocket.websocket { BaseBackplane, MemoryBackplane }
    scale.websocket.protocol --> scale.server.websocket_ext { AUTH_HANDSHAKE_TIMEOUT_SECONDS, HEARTBEAT_MISSED_ALLOWED, HEARTBEAT_SECONDS, SEND_TIMEOUT_SECONDS, ws_authenticate, ws_error_frame, ws_execute_target, ws_handle_control, ws_heartbeat_loop, ws_pre_accept_auth, ws_receive_frame, ws_reject_auth, ws_reject_pre_accept, ws_reject_registration }
    scale.websocket.protocol --> scale.tests.server.test_ws_hardening { ws_handle_control, ws_heartbeat_loop }
    scale.websocket.websocket --> scale.server.websocket_ext { ConnectionContext, WebSocketConnectionManager, _ws_stream_result }
    scale.websocket.websocket --> scale.tests.server.test_ws_hardening { ConnectionContext, WebSocketConnectionManager }
    scale.websocket.websocket --> scale.websocket.protocol { ConnectionContext, consume_rate_token }
    server.assembly --> cli.commands.execution { gateway_colocates as _gateway_colocates, service_apps as _service_apps }
    server.assembly --> cli.commands.execution.serve { service_apps }
    server.assembly --> dist.precompile_bytecode._application_sources { service_apps }
    server.assembly --> dist.seal.build_serve_manifest { service_apps }
    server.assembly --> dist.source.project.export_project { gateway_colocates, service_apps }
    server.assembly --> runtime.prepared.initialize_application { assemble_served_program }
    server.assembly --> scale.server.inprocess.prepare_inprocess_runtime { service_apps }
    server.bridge --> scale.tests.data.test_eager_spawn { BridgeUnavailable }
    server.bridge --> scale.tests.server.test_sv_streaming { BridgeError }
    server.bridge --> server.outbox { BridgeRejected }
    server.bridge --> server.outbox.remember_response { serialize_response }
    server.bridge --> server.outbox.replay_cached { replay_response }
    server.bridge --> server.sv_client { BridgeError, BridgeUnavailable, bridge_error_for_status, bridge_error_from }
    server.build_status --> cli.commands.execution { BuildMonitor }
    server.build_status --> scale.tests.server.test_build_status_endpoint { BuildMonitor }
    server.build_status --> server.endpoints.pages.register_diagnostics_endpoints.build_status { get_build_status }
    server.build_status --> server.hmr { BuildMonitor, BuildStatus }
    server.endpoint_contract --> server.endpoints.colocated { check_endpoint_contract }
    server.endpoint_contract --> server.endpoints.walkers { check_endpoint_contract }
    server.hmr --> cli.commands.execution._start_vite_dev_server { HotReloader }
    server.hmr --> cli.commands.execution.serve { HotReloader }
    type server.hmr --> compiler.driver.build_services { HotReloader }
    server.hmr --> compiler.driver.build_services.CompilerBuildServices.hot_reloader { HotReloader }
    type server.hmr --> runtime.build_services { HotReloader }
    server.hmr --> scale.tests.server.test_build_status_endpoint { HotReloader }
    type server.hmr --> server.build_status { HotReloader }
    type server.hmr --> testing.testing { HotReloader }
    server.middleware --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway._install_admin_api { jwt_middleware }
    server.middleware --> scale.server.jobs_ext { require_user }
    server.middleware --> scale.server.sso_ext { require_user }
    server.middleware --> server.endpoints.auth { require_user }
    server.middleware --> server.endpoints.introspection { unauthorized }
    server.middleware --> server.server.JacAPIServer._install_middleware { jwt_middleware, request_context_middleware }
    server.middleware --> server.server.JacAPIServer.build_app { metrics_middleware }
    server.net --> cli.commands.execution._find_free_port { find_available_port }
    server.net --> cli.commands.execution.serve { PortInUseError }
    server.net --> cli.errmap.humanize_error { PortInUseError }
    server.net --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.start { PORT_RETRY_LIMIT }
    server.net --> scale.tests.server.test_serve { ERRNO_ADDR_IN_USE, PORT_RETRY_LIMIT, PortInUseError, find_available_port as _find_available_port }
    server.net --> server.server { PORT_RETRY_LIMIT }
    server.net --> server.serving.server { PORT_RETRY_LIMIT, bind_listener }
    server.net --> server.serving.supervisor { PORT_RETRY_LIMIT, bind_listener }
    server.outbox --> scale.tests.server.test_sv_outbox_endpoints { LEASE_S, OutboxEntry, PgOutboxStore, STATUS_DELIVERED, STATUS_DELIVERING, STATUS_PENDING, SqliteOutboxStore, stop_worker, use_store, worker_running }
    server.outbox --> scale.tests.server.test_sv_streaming { STATUS_DELIVERED, SqliteOutboxStore, default_idempotency_key, deliver_pending, enqueue, use_store }
    server.outbox --> server.endpoints.colocated { remember_response, replay_cached }
    server.outbox --> server.endpoints.walkers { remember_response, replay_cached, scoped_idempotency_key }
    server.outbox --> server.server.JacAPIServer._worker_main { start_worker_if_bridging, stop_worker }
    server.outbox --> server.server.JacAPIServer.serve_background { start_worker_if_bridging, stop_worker }
    server.outbox --> server.sv_client.spawn_deferred { enqueue }
    server.sealed_serve --> cli.commands.execution._jab_native_bin { NATIVE_DIR_REL }
    server.sealed_serve --> client.artifact.client_output_dir { client_dist_for }
    server.sealed_serve --> client.artifact.prebuilt_bundle { client_dist_for, serve_manifest_for }
    server.sealed_serve --> compiler.driver.application._prepare_sealed { CLIENT_DIST_REL, SERVE_MANIFEST_REL }
    server.sealed_serve --> compiler.driver.application.prepare_application { sealed_root_for, unlisted_image_root }
    server.sealed_serve --> dist.precompile_bytecode.app_metadata { CLIENT_DIST_REL, NATIVE_DIR_REL }
    server.sealed_serve --> dist.precompile_bytecode.collect_payloads { CLIENT_DIST_REL, NATIVE_DIR_REL, SERVE_MANIFEST_REL }
    server.sealed_serve --> dist.precompile_bytecode.seal_native { NATIVE_DIR_REL }
    server.sealed_serve --> dist.precompile_bytecode.seal_runtime_closure { SERVE_MANIFEST_REL }
    server.sealed_serve --> dist.seal.bake_native_payloads { NATIVE_DIR_REL }
    server.sealed_serve --> dist.seal.bake_serve_payloads { CLIENT_DIST_REL, SERVE_MANIFEST_REL }
    server.sealed_serve --> scale.injector.bundle.pack_jab { SERVE_MANIFEST_REL }
    server.sealed_serve --> server.endpoints.pages._static_base { sealed_root_for }
    server.sealed_serve --> server.endpoints.pages.register_page_endpoints { client_dist_for }
    server.sealed_serve --> server.server.ModuleIntrospector._load_manifest { serve_manifest_for }
    server.sealed_serve --> server.server.ModuleIntrospector._load_spa_routes { serve_manifest_for }
    server.sealed_serve --> server.server.ModuleIntrospector._load_surface { serve_manifest_for }
    server.sealed_serve --> server.server.ModuleIntrospector._resolve_declared { sealed_root_for }
    type server.server --> client.serving { ModuleIntrospector }
    server.server --> client.targets.client_dev_common.dev_proxy_paths { ModuleIntrospector }
    server.server --> client.targets.desktop.native.broker_extension { JacAPIServer, ServerExtension }
    type server.server --> runtime.builtin.restspec { JacAPIServer }
    type server.server --> runtime.runtime { JacAPIServer as JacServer, ModuleIntrospector, ServerExtension }
    server.server --> runtime.runtime.JacServe.get_api_server_class { JacAPIServer }
    server.server --> runtime.source_app.main { JacAPIServer }
    server.server --> scale.admin.admin_portal { EndpointHost, JsonValue }
    server.server --> scale.admin.deploy_health { EndpointHost }
    server.server --> scale.admin.llm_telemetry { EndpointHost, JsonValue }
    server.server --> scale.admin.logs { EndpointHost }
    server.server --> scale.admin.network { EndpointHost }
    server.server --> scale.admin.ops { EndpointHost }
    server.server --> scale.admin.podenv { EndpointHost }
    server.server --> scale.admin.traces { EndpointHost }
    server.server --> scale.admin.workloads { EndpointHost }
    server.server --> scale.plugin { JacAPIServer as JacServer, ServerExtension }
    server.server --> scale.runtime.gateway.microservice_gateway { EndpointHost }
    type server.server --> scale.runtime.provider { JacAPIServer as JacServer, ServerExtension }
    server.server --> scale.server.extensions { JacAPIServer, ServerExtension }
    server.server --> scale.server.inprocess { JacAPIServer, ServerExtension }
    server.server --> scale.server.jobs_ext { JacAPIServer, ServerExtension }
    server.server --> scale.server.sso_ext { JacAPIServer, ServerExtension }
    server.server --> scale.server.webhook_ext { JacAPIServer, JsonValue, ServerExtension }
    server.server --> scale.server.websocket_ext { JacAPIServer, ServerExtension }
    server.server --> scale.tests.data.test_eager_spawn { JacAPIServer }
    server.server --> scale.tests.data.test_identity_fail_loud { JacAPIServer }
    server.server --> scale.tests.microservices.test_microservice { JacAPIServer }
    server.server --> scale.tests.server.test_host_serving { JacAPIServer }
    server.server --> scale.tests.server.test_served_app_route { JacAPIServer }
    server.server --> scale.tests.server.test_sso { EndpointHost }
    server.server --> scale.tests.server.test_sv_outbox_endpoints { JacAPIServer }
    server.server --> scale.tests.support { EndpointHost }
    server.server --> server.endpoints.auth { EndpointHost, JsonValue }
    server.server --> server.endpoints.colocated { JacAPIServer, JsonValue, ModuleIntrospector }
    server.server --> server.endpoints.introspection { JacAPIServer }
    server.server --> server.endpoints.pages { JacAPIServer, JsonValue }
    server.server --> server.endpoints.walkers { JacAPIServer, JsonValue, target_restspec }
    server.server --> testing.testing { JacAPIServer }
    type server.server --> testing.testing { JacAPIServer }
    server.session --> cli.commands.db._db_status { conninfo_from_url }
    server.session --> cli.commands.db._open_project_store { conninfo_from_url }
    server.session --> cli.commands.db._project_data_dir { shared_pg_data_dir }
    server.session --> cli.commands.db._project_database { project_db_name }
    server.session --> cli.commands.db._runtime_for { scratch_owner_pid }
    server.session --> cli.commands.execution.serve { takeover_project }
    server.session --> data.query_planner { Session }
    server.session --> runtime.context.ExecutionContext.__post_init__ { Session }
    server.session --> runtime.runtime.JacGraph.refs { Session }
    server.session --> scale.events.streams.postgres.PgEventStream._ensure_store { conninfo_from_url }
    server.session --> scale.injector.bundle.seal_step_env { SCRATCH_ENV }
    server.session --> scale.memory.context.JScaleExecutionContext.init { Session, conninfo_from_url, promotions_for }
    server.session --> scale.tests.data.test_pg_stream { shared_pg_data_dir }
    server.session --> scale.tests.deploy.test_postgres_predicate_lock_headroom { shared_pg_data_dir }
    server.session --> scale.tests.microservices.test_app_precompile { SCRATCH_ENV }
    server.session --> scale.tests.server.test_scheduler_multipod._unreachable_store { conninfo_from_url }
    server.session --> scale.tests.server.test_sv_outbox_endpoints { Session }
    server.session --> server.outbox._writable_txn { Session }
    server.session --> server.shared_store.shared_store { conninfo_from_url, promotions_for, runtime_for_base }
    server.session --> testing.test_runner._fresh_jac_state { mark_scratch_base }
    server.session --> testing.test_runner.run_tests { own_child_databases }
    server.settings --> cli.commands.execution.serve { ServeConfigError, ServeSettings }
    server.settings --> runtime.source_app.main { ServeSettings }
    server.settings --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway._install_admin_api { ServeSettings }
    server.settings --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.start { ServeSettings }
    server.settings --> scale.server.inprocess { ServeSettings }
    server.settings --> scale.tests.data.test_dev_signing_secret { ServeConfigError, ServeSettings }
    server.settings --> scale.tests.microservices.test_drain { ServeSettings }
    server.settings --> scale.tests.server.test_host_serving { ServeSettings }
    server.settings --> scale.tests.server.test_registration_challenge { AuthSettings }
    server.settings --> scale.tests.server.test_registration_limits { AuthSettings }
    server.settings --> scale.tests.server.test_serve { ServeSettings }
    server.settings --> scale.tests.server.test_serving_tail { ServeSettings }
    server.settings --> server.identity.config { AuthSettings }
    server.settings --> server.server { ServeSettings }
    server.settings --> server.server.JacAPIServer._validate_or_raise { ServeConfigError }
    server.settings --> server.serving.server { ServeSettings }
    server.settings --> server.serving.supervisor { ServeSettings }
    server.shared_store --> scale.admin.ops._postgres_ping_blocking { NO_DATABASE_RESOLVED, shared_store, shared_store_failure }
    server.shared_store --> scale.events.streams.postgres.PgEventStream._ensure_store { scale_db_url }
    server.shared_store --> scale.memory.context.JScaleExecutionContext.init { scale_db_url }
    server.shared_store --> scale.runtime.provider { shared_store as _pg_anchor }
    server.shared_store --> scale.scheduler.scheduler { shared_store }
    server.shared_store --> scale.server.extensions.EventsExtension.register { scale_db_url }
    server.shared_store --> scale.server.extensions.EventsExtension.validate { scale_db_url }
    server.shared_store --> scale.sso.oauth_session.OAuthSession.complete_native { shared_store }
    server.shared_store --> scale.sso.oauth_session.OAuthSession.poll { shared_store }
    server.shared_store --> scale.state.factory { shared_store, shared_store_failure }
    server.shared_store as pg_mod --> scale.tests.misc.test_shared_store_failure;
    server.shared_store as store_mod --> scale.tests.misc.test_state_backend_selection;
    server.shared_store --> scale.tests.server.test_oauth_session { shared_store }
    server.shared_store --> scale.webhook.webhook { shared_store }
    server.shared_store --> scale.websocket.backplane.PgBackplane.start { shared_store }
    server.shared_store --> scale.websocket.backplane.build_backplane { scale_db_url }
    server.shared_store --> server.identity.auth_tokens.AuthTokenStore.__post_init__ { shared_store }
    server.shared_store --> server.identity.rate_limit { shared_store }
    server.shared_store --> server.identity.user_manager.UserManager.__post_init__ { NO_DATABASE_RESOLVED, shared_store, shared_store_failure }
    server.static_files --> server.endpoints.pages { client_dist_index, find_root_asset, find_static_candidate, sibling_app_dist, sibling_app_file }
    server.static_files --> server.server.print_endpoint_docs { sibling_app_names }
    server.sv_client --> client.targets.client_dev_common { headless_start_args }
    server.sv_client --> scale.runtime.orchestrator.process_manager.ServiceProcessManager.start_service { app_start_args, headless_start_args, peer_url_env_key }
    server.sv_client --> scale.tests.deploy.test_pod_env { peer_url_env_key }
    server.sv_client --> server.assembly.assemble_served_program { set_consumer_app }
    server.sv_client --> server.assembly.colocate_services { register_local }
    server.sv_client --> server.endpoints.colocated { _local_providers }
    server.sv_client --> server.endpoints.colocated.served_app_route { consumer_app }
    server.sv_client --> server.endpoints.walkers { IDEMPOTENCY_HEADER, bridge_identity }
    server.sv_client --> server.endpoints.walkers.function_callback.callback { consumer_app }
    server.sv_client --> server.endpoints.walkers.walker_callback.callback { consumer_app }
    server.sv_client as sv_client --> server.outbox._deliver_one;
    server.sv_client as sv_client --> server.outbox.start_worker_if_bridging;
    server.task_scheduler --> runtime.builtin.schedule { ScheduleSpec }
    server.task_scheduler --> scale.scheduler.scheduler { ScheduleTrigger, Scheduler, schedule_namespace, tick_of }
    server.task_scheduler --> scale.tests.server.test_scheduler_multipod { tick_of }
    server.task_scheduler --> server.server { Scheduler }
    server.task_scheduler --> server.server.JacAPIServer.__post_init__ { Scheduler }
    server.task_scheduler --> server.server.JacAPIServer._register_scheduled_tasks { schedule_namespace }
    server.task_scheduler --> server.server.JacAPIServer._scheduled_targets { ScheduleSpec }
    server.task_scheduler --> server.server.ModuleIntrospector.scheduled_members { ScheduleSpec }
    server.transport --> scale.admin.admin_portal { Meta, TransportResponse }
    server.transport --> scale.admin.llm_telemetry { Meta, TransportResponse }
    server.transport --> scale.admin.logs { TransportResponse }
    server.transport --> scale.admin.workloads { Meta, TransportResponse }
    server.transport --> scale.server.jobs_ext { Meta, TransportResponse }
    server.transport --> scale.server.sso_ext { TransportResponse }
    server.transport --> scale.server.webhook_ext { Meta, TransportResponse }
    server.transport --> scale.shared.utils { Meta, TransportResponse }
    server.transport --> scale.sso.sso_auth { Meta, TransportResponse }
    server.transport --> scale.tests.server.test_firebase_auth_sso { TransportResponse }
    server.transport --> scale.tests.server.test_sso { Meta, TransportResponse }
    server.transport --> scale.webhook.webhook { Meta, TransportResponse }
    server.transport --> server.bridge.serialize_response { TransportResponse }
    server.transport --> server.endpoint_contract { Meta, TransportResponse }
    server.transport --> server.endpoints.auth { Meta, TransportResponse }
    server.transport --> server.endpoints.colocated { Meta, TransportResponse }
    server.transport --> server.endpoints.introspection { Meta, TransportResponse }
    server.transport --> server.endpoints.walkers { Meta, TransportResponse }
    server.transport --> server.middleware { Meta, TransportResponse }
    server.transport --> server.outbox.remember_response { TransportResponse }
    server.transport --> server.serving.app { TransportResponse }
    server.watcher --> cli.commands.execution.serve { JacFileWatcher }
    server.watcher --> client.targets.client_dev_common { FileChangeEvent }
    server.watcher --> client.targets.desktop.webview_shell.webview_dev { JacFileWatcher }
    server.watcher --> client.targets.mobile_target { FileChangeEvent }
    server.watcher --> client.targets.mobile_target.MobileTarget.dev { JacFileWatcher }
    server.watcher --> client.targets.react_native.dev { FileChangeEvent }
    server.watcher --> client.targets.web_target.WebTarget.dev { JacFileWatcher }
    server.watcher --> compiler.driver.build_services.CompilerBuildServices.hot_reloader { JacFileWatcher }
    server.watcher --> scale.tests.server.test_build_status_endpoint { JacFileWatcher }
    type server.watcher --> server.hmr { ChangeType, FileChangeEvent, JacFileWatcher }
    server.session --> cli.commands.db._project_target { project_db_name }
    server.task_scheduler --> scale.tests.server.test_scheduler_multipod { ScheduleSpec, Scheduler }
    server.exchange --> scale.tests.server.test_restspec { current_request, respond }
    server.exchange --> server.endpoints.colocated { refusal_status, settle_envelope }
    server.exchange --> server.endpoints.walkers { refusal_status, settle_envelope }
    server.exchange --> server.middleware { close_exchange, open_exchange }
    server.exchange --> server.server { forget_response_choice }
    server.middleware --> scale.tests.data.test_gateway_owned_identity { jwt_middleware }
    server.middleware --> server.endpoints.auth { bearer_token }
    server.middleware --> server.endpoints.second_factor { bearer_token, require_user }
    server.server --> server.endpoints.second_factor { EndpointHost, JsonValue }
    server.settings --> scale.deploy.target.kubernetes.manifest_builder { resolve_count }
    server.settings --> scale.tests.deploy.test_deployment_overlay { ServeConfigError }
    server.shared_store --> server.identity.second_factor { shared_store }
    server.transport --> server.exchange | server.endpoints.second_factor { TransportResponse }
    server.exchange --> server.endpoints.walkers { apply_response_choice, has_response_choice }
    server.request_scope --> scale.server.websocket_ext { RequestScope }
    server.request_scope --> server.middleware { RequestScope }
    server.request_scope --> server.server { RequestScope }
    server.server --> runtime.builtin.restspec { restspec_fields }
    server.server --> scale.tests.server.test_auth_policy_startup { EndpointHost, ServerExtension }
    server.session --> server.server._run_function_with_occ { Session, transient_db_error }
    server.settings --> scale.deploy.target.kubernetes.manifest_builder { AuthSettings }
    server.settings --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway._install_admin_api { ServeConfigError }
    server.settings --> scale.tests.server.test_auth_policy_http { ServeConfigError }
    server.settings --> scale.tests.server.test_auth_policy_startup { AuthSettings, EmailSettings, LockoutSettings, PasswordSettings }
    server.settings --> scale.tests.server.test_oauth_session { AuthSettings, EmailSettings, IdentifierSettings, LockoutSettings, PasswordSettings, RegistrationSettings }
    server.settings --> scale.tests.server.test_registration_challenge { RegistrationSettings }
    server.settings --> scale.tests.server.test_registration_limits { RegistrationSettings }
    server.settings --> scale.tests.server.test_sso { AuthSettings, IdentifierSettings }
    server.settings --> scale.tests.server.test_sv_outbox_endpoints { ServeSettings }
    server.settings --> server.identity.policy { IDENTIFIER_KINDS, PASSWORD_CLASSES, PasswordSettings }
    server.settings --> server.identity.user_manager { IDENTIFIER_KINDS, in_cluster }
    server.settings --> server.server.JacAPIServer._validate_or_raise { default_threads }
    server.settings --> server.server.JacAPIServer.serve_background { default_threads }
    server.task_scheduler --> server.server.JacAPIServer._start_problems { schedule_problems }
    server.watcher --> cli.commands.execution.serve { application_watch_roots }
    server.endpoints.auth --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway._install_admin_api { register_auth_endpoints }
    server.endpoints.auth --> scale.tests.server.test_registration_challenge { register_auth_endpoints }
    server.endpoints.auth --> scale.tests.server.test_registration_limits { register_auth_endpoints }
    server.endpoints.auth --> server.server.JacAPIServer.register_endpoints { register_auth_endpoints }
    server.endpoints.colocated --> scale.tests.server.test_sv_outbox_endpoints { register_colocated_endpoints }
    server.endpoints.colocated --> server.server.JacAPIServer.register_endpoints { register_colocated_endpoints }
    server.endpoints.colocated --> server.server.print_endpoint_docs { colocated_providers, provider_route }
    server.endpoints.introspection --> server.server.JacAPIServer.register_endpoints { register_introspection_endpoints }
    server.endpoints.pages --> scale.tests.server.test_build_status_endpoint { register_diagnostics_endpoints }
    server.endpoints.pages --> server.server.JacAPIServer.register_endpoints { register_diagnostics_endpoints, register_graph_endpoints, register_page_endpoints }
    server.endpoints.walkers --> server.endpoints.colocated { idempotency_key, request_caller }
    server.endpoints.walkers --> server.server.JacAPIServer.register_endpoints { register_function_endpoints, register_walker_endpoints }
    server.endpoints.auth --> server.endpoints.second_factor { fail, ok }
    server.endpoints.second_factor --> server.endpoints.auth.register_auth_endpoints { register_second_factor_endpoints }
    server.endpoints.auth --> scale.admin.admin_portal { refused, throttled }
    server.endpoints.auth --> scale.server.extensions { register_mail_endpoints }
    server.endpoints.auth --> server.endpoints.second_factor { throttled }
    server.identity.audit --> server.endpoints.auth { client_ip, emit as audit }
    server.identity.auth_models --> scale.server.sso_ext { FirebaseTokenRequest }
    server.identity.auth_models --> scale.tests.server.test_registration_challenge { RegisterRequest }
    server.identity.auth_models --> scale.tests.server.test_registration_limits { RegisterRequest }
    server.identity.auth_models --> server.endpoints.auth { AddIdentityRequest, LoginRequest, MeIdentity, MeResponse, RegisterRequest, ResetPasswordRequest, UpdatePasswordRequest, UpdateProfileRequest, UpdateProfileResponse, UpdateUsernameRequest, VerifyIdentityRequest }
    server.identity.auth_tokens --> scale.sso.oauth_session { AuthTokenStore }
    server.identity.auth_tokens --> scale.sso.sso_auth { AuthTokenStore }
    server.identity.auth_tokens --> scale.tests.data.test_auth_tokens_fail_closed { AuthTokenStore, reset_auth_token_store }
    server.identity.auth_tokens --> scale.tests.server.test_emailer_factory { AuthTokenStore, reset_auth_token_store }
    server.identity.auth_tokens --> scale.tests.server.test_oauth_session { AuthTokenStore }
    server.identity.auth_tokens --> scale.tests.server.test_registration_challenge { AuthTokenStore }
    server.identity.auth_tokens --> scale.tests.server.test_sso { AuthTokenStore }
    server.identity.auth_tokens --> server.endpoints.auth { AuthTokenStore }
    server.identity.auth_tokens --> server.identity.app_tokens { AuthTokenStore }
    server.identity.auth_tokens --> server.identity.registration_challenge { AuthTokenStore }
    server.identity.config --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway._install_admin_api { configure_identity }
    server.identity.config --> scale.tests.data.test_gateway_owned_identity { signing_algorithm as jwt_algorithm, signing_secret as jwt_secret }
    server.identity.config --> scale.tests.microservices.test_microservice { signing_algorithm as jwt_algorithm, signing_secret as jwt_secret }
    server.identity.config --> scale.tests.server.test_serve { signing_secret as jwt_secret }
    server.identity.config --> scale.webhook.webhook.WebhookUtils.create_api_key_token { signing_algorithm, signing_secret }
    server.identity.config --> scale.webhook.webhook.WebhookUtils.validate_api_key { signing_algorithm, signing_secret }
    server.identity.config --> server.endpoints.auth { auth_settings }
    server.identity.config --> server.identity.identity_storage { password_hash_cost }
    server.identity.config --> server.identity.user_manager { signing_algorithm, signing_secret, token_ttl_days }
    server.identity.config --> server.server.JacAPIServer.__post_init__ { configure_identity, signing_secret }
    server.identity.identity_storage --> scale.sso.oauth_session { primary_username }
    server.identity.identity_storage --> scale.tests.data.test_auth_cutover { PgIdentityStorage }
    server.identity.identity_storage as storage_mod --> scale.tests.data.test_identity_fail_loud;
    server.identity.identity_storage --> scale.tests.data.test_identity_password { IdentityStorage }
    server.identity.identity_storage --> server.endpoints.auth { primary_username }
    server.identity.identity_storage --> server.identity.user_manager { IdentityStorage, PgIdentityStorage }
    server.identity.identity_storage --> server.server.JacAPIServer._register_scheduled_tasks { PgIdentityStorage }
    server.identity.rate_limit --> scale.tests.server.test_registration_limits { consume_limit }
    server.identity.rate_limit --> server.endpoints.auth { consume_limit }
    server.identity.registration_challenge --> scale.tests.server.test_registration_challenge { consume_challenge, issue_challenge }
    server.identity.registration_challenge --> server.endpoints.auth { consume_challenge, issue_challenge }
    type server.identity.user_manager --> runtime.runtime { UserManager }
    server.identity.user_manager --> runtime.runtime.JacPersistence.get_user_manager { UserManager }
    server.identity.user_manager --> scale.admin.admin_portal { UserManager, UserRole }
    server.identity.user_manager --> scale.runtime.gateway.microservice_gateway { UserManager }
    server.identity.user_manager --> scale.server.jobs_ext { SYSTEM_USER, UserRole }
    server.identity.user_manager --> scale.server.webhook_ext { SYSTEM_USER }
    server.identity.user_manager --> scale.sso.oauth_session { UserManager }
    server.identity.user_manager --> scale.sso.sso_auth { UserManager }
    server.identity.user_manager --> scale.tests.data.test_gateway_owned_identity { UserManager }
    server.identity.user_manager --> scale.tests.data.test_identity_fail_loud { UserManager }
    server.identity.user_manager --> scale.tests.misc.test_shared_store_failure { UserManager }
    server.identity.user_manager --> scale.tests.server.test_firebase_auth_sso { UserManager }
    server.identity.user_manager --> scale.tests.server.test_oauth_session { UserManager }
    server.identity.user_manager --> scale.tests.server.test_sso { UserManager }
    server.identity.user_manager --> scale.tests.server.test_ws_hardening { UserManager }
    server.identity.user_manager --> scale.tests.support { UserManager }
    server.identity.user_manager --> server.endpoints.auth { UserRole }
    server.identity.user_manager --> server.middleware { UserManager }
    server.identity.user_manager --> server.server { UserManager }
    server.identity.user_manager --> server.server.JacAPIServer._ensure_internal_users { SYSTEM_USER, UserRole }
    server.identity.user_manager --> server.server.JacAPIServer._register_scheduled_tasks { SYSTEM_USER }
    server.identity.assurance --> scale.admin.admin_portal { METHOD_PASSWORD, second_factor_claims }
    server.identity.assurance --> scale.tests.data.test_gateway_owned_identity { caller_assurance_level, second_factor_claims }
    server.identity.assurance --> server.endpoints.second_factor { AAL1, AAL2, METHOD_PASSWORD, METHOD_TOTP, second_factor_claims, token_assurance }
    server.identity.assurance --> server.identity.second_factor { METHOD_RECOVERY, METHOD_TOTP }
    server.identity.assurance --> server.identity.user_manager { carried_claims }
    server.identity.assurance --> server.middleware { bind_caller_assurance, release_caller_assurance, token_assurance }
    server.identity.audit --> server.endpoints.second_factor { client_ip, emit as audit }
    server.identity.auth_models --> server.endpoints.second_factor { EnrollFactorRequest, RemoveFactorRequest, SecondFactorLoginRequest, VerifyFactorRequest }
    server.identity.auth_tokens --> server.identity.second_factor { AuthTokenStore }
    server.identity.config --> scale.tests.server.test_admin { signing_secret }
    server.identity.config --> server.identity.assurance { signing_algorithm, signing_secret }
    server.identity.config --> server.identity.second_factor { auth_settings }
    server.identity.config --> server.identity.session_cookie { auth_settings, token_ttl_days }
    server.identity.identity_storage --> server.endpoints.second_factor { primary_username }
    server.identity.identity_storage --> server.identity.second_factor { IdentityStorage }
    server.identity.rate_limit --> server.identity.second_factor { consume_limit, refund_limit }
    server.identity.second_factor --> scale.admin.admin_portal { SecondFactorUnavailable }
    server.identity.second_factor --> server.endpoints.second_factor { FACTOR_VERIFIED, SecondFactorUnavailable }
    server.identity.second_factor --> server.identity.user_manager { SecondFactorManager }
    server.identity.session_cookie --> server.endpoints.auth { end_session, start_session }
    server.identity.session_cookie --> server.endpoints.second_factor { start_session }
    server.identity.session_cookie --> server.middleware { apply_session_change, cookie_session_token, keep_out_of_shared_caches }
    server.identity.totp --> server.identity.second_factor { matching_step, new_totp_secret, provisioning_uri }
    server.identity.user_manager --> server.endpoints.second_factor { UserRole }
    server.identity.assurance --> scale.sso.oauth_session { METHOD_FEDERATED }
    server.identity.assurance --> server.identity.second_factor { METHOD_PASSWORD }
    server.identity.assurance --> server.identity.user_manager { METHOD_PASSWORD }
    server.identity.audit --> scale.admin.admin_portal { client_ip }
    server.identity.audit --> server.identity.mail { emit as audit }
    server.identity.auth_models --> scale.admin.admin_portal { IdentityInputModel }
    server.identity.auth_models --> server.endpoints.auth { ForgotPasswordRequest, SendVerificationRequest }
    server.identity.auth_tokens --> server.identity.mail { AuthTokenStore }
    server.identity.auth_tokens --> server.identity.user_manager { AuthTokenStore }
    server.identity.common_passwords --> server.identity.policy { COMMON_PASSWORDS }
    server.identity.config --> scale.sso.github { auth_settings }
    server.identity.config --> scale.sso.oauth_session { auth_settings }
    server.identity.config --> scale.tests.server.test_auth_policy_startup { configure_identity }
    server.identity.config --> scale.tests.server.test_oauth_session { configure_identity }
    server.identity.config --> scale.tests.server.test_sso { configure_identity }
    server.identity.config --> server.identity.identity_storage { auth_settings }
    server.identity.config --> server.identity.mail { auth_settings }
    server.identity.config --> server.identity.policy { auth_settings }
    server.identity.config --> server.identity.user_manager { auth_settings }
    server.identity.identity_storage --> server.identity.user_manager { IdentityTakenError }
    server.identity.mail --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway._install_admin_api { verification_problems }
    server.identity.mail --> scale.tests.server.test_auth_policy_startup { verification_problems }
    server.identity.mail --> server.endpoints.auth { MailOutcome, VERIFY_PURPOSE }
    server.identity.mail --> server.identity.user_manager { RESET_PURPOSE }
    server.identity.mail --> server.server { IdentityMailer, verification_problems }
    server.identity.policy --> scale.deploy.target.kubernetes.target { minted_password }
    server.identity.policy --> scale.server.extensions { check_password }
    server.identity.policy --> scale.sso.oauth_session { check_email }
    server.identity.policy --> scale.tests.server.test_auth_policy_startup { check_password, minted_password }
    server.identity.policy --> server.endpoints.auth { POLICY_VIOLATION, public_policy }
    server.identity.policy --> server.identity.identity_storage { VERIFY_BEFORE_LOGIN, verify_before_login }
    server.identity.policy --> server.identity.user_manager { Violation, awaiting_verification, check_identifiers, check_identity, check_password, minted_password, refusal }
    server.identity.rate_limit --> scale.admin.admin_portal { AttemptsExhausted }
    server.identity.rate_limit --> server.endpoints.auth { AttemptsExhausted }
    server.identity.rate_limit --> server.identity.mail { consume_limit }
    server.identity.rate_limit --> server.identity.user_manager { AttemptsExhausted, consume_limit, refund_limit }
    server.identity.user_manager --> scale.tests.server.oauth_fixtures { SessionGrant }
    server.identity.user_manager --> scale.tests.server.test_auth_policy_startup { UserManager }
    server.identity.user_manager --> scale.tests.server.test_oauth_session { SecondFactorRequired, SessionGrant }
    server.identity.user_manager --> scale.tests.server.test_registration_challenge { SessionGrant }
    server.serving.accesslog --> scale.tests.server.test_serve { ACCESS_LOGGER_NAME, AccessJsonFormatter, AccessRecord, HealthCheckFilter, access_logger, configure_access_logging }
    server.serving.accesslog --> server.server.JacAPIServer._prepare_to_serve { configure_access_logging }
    server.serving.accesslog --> server.serving.server { AccessRecord, emit as emit_access }
    server.serving.app --> scale.runtime.gateway.embedded_gateway { ServingApp }
    server.serving.app --> scale.runtime.gateway.microservice_gateway { ServingApp }
    server.serving.app --> scale.tests.microservices.test_drain { ServingApp }
    server.serving.app --> scale.tests.microservices.test_gateway_webapp { ServingApp }
    server.serving.app --> scale.tests.server.test_bodiless_status { ServingApp }
    server.serving.app --> scale.tests.server.test_registration_limits { transport_to_response }
    server.serving.app --> scale.tests.server.test_serving_tail { ServingApp }
    server.serving.app --> scale.tests.server.test_stream_ws._spawn_upstream { ServingApp }
    server.serving.app --> scale.tests.server.test_stream_ws._spawn_ws_upstream { ServingApp }
    server.serving.app --> scale.tests.server.test_stream_ws._spawn_ws_upstream_with_protocol { ServingApp }
    server.serving.app --> server.bridge.serialize_response { transport_to_response }
    server.serving.app --> server.server { ServingApp }
    server.serving.app --> server.serving.health { ServingApp }
    server.serving.app --> server.serving.openapi { ServingApp }
    server.serving.app --> server.serving.server { ServingApp }
    server.serving.app --> testing.testkit { ServingApp }
    server.serving.authcrypt as ac --> scale.tests.data.test_auth_cutover;
    server.serving.authcrypt --> scale.tests.data.test_auth_cutover { SCRYPT_MAXMEM, SCRYPT_MAX_N, hash_password, is_prescrypt_hash, verify_password }
    server.serving.authcrypt --> scale.tests.data.test_dev_signing_secret { PLACEHOLDER_JWT_SECRET, jwt_decode, jwt_encode, project_data_dir, project_signing_secret }
    server.serving.authcrypt --> scale.tests.data.test_gateway_owned_identity { jwt_encode }
    server.serving.authcrypt --> scale.tests.microservices.test_microservice { jwt_encode }
    server.serving.authcrypt --> scale.tests.server.test_oauth_providers { jwt_encode }
    server.serving.authcrypt --> scale.tests.server.test_serve { jwt_decode as _jwt_decode, jwt_encode as _jwt_encode }
    server.serving.authcrypt --> scale.webhook.webhook { JWTError, JWTExpiredError, jwt_decode, jwt_encode }
    server.serving.authcrypt --> server.identity.identity_storage { hash_password as _scrypt_hash, is_prescrypt_hash as _is_prescrypt, needs_rehash as _needs_rehash, verify_password as _scrypt_verify }
    server.serving.authcrypt --> server.identity.user_manager { JWTError, JWTExpiredError, jwt_decode, jwt_encode }
    server.serving.authcrypt --> server.settings.AuthSettings.resolve_secret { PLACEHOLDER_JWT_SECRET, project_signing_secret }
    server.serving.client --> scale.admin.logs._loki_request { ClientConnectionError, arequest }
    server.serving.client --> scale.admin.ops._http_ready { arequest }
    server.serving.client --> scale.admin.ops._loki_recent_count { arequest }
    server.serving.client --> scale.admin.ops._tempo_recent_count { arequest }
    server.serving.client --> scale.admin.traces._tempo_request { ClientConnectionError, arequest }
    server.serving.client --> scale.runtime.middleware.ws_forward { ClientConnectionError, aws_connect }
    server.serving.client --> scale.runtime.rpc.rpc._rpc_with_retries { ClientConnectionError, ClientRequestNotSent }
    server.serving.client --> scale.runtime.rpc.rpc.service_call { post_stream_aware_sync }
    server.serving.client --> scale.runtime.rpc.rpc.walker_call { request_sync }
    server.serving.client --> scale.runtime.transport.http_forward { ClientConnectionError, arequest }
    server.serving.client --> scale.sso.github { arequest }
    server.serving.client --> scale.sso.google { arequest }
    server.serving.client --> scale.sso.provider { arequest }
    server.serving.client --> scale.tests.server.test_serve { aws_connect }
    server.serving.client as sv_http --> scale.tests.server.test_sv_auth_forward;
    server.serving.client --> scale.tests.server.test_sv_auth_forward._install_unreachable_transport { ClientRequestNotSent }
    server.serving.client --> scale.tests.server.test_sv_auth_forward._install_unreachable_walker_transport { ClientRequestNotSent }
    server.serving.client --> server.bridge.bridge_error_from { ClientConnectionError, ClientReadTimeout, ClientRequestNotSent }
    server.serving.client --> server.sv_client._http_call { post_stream_aware_sync }
    server.serving.client --> server.sv_client._http_spawn { request_sync }
    server.serving.client --> testing.testing { run_blocking }
    server.serving.client --> testing.testkit { aws_connect, run_blocking }
    server.serving.coerce --> server.endpoints.walkers { is_upload_type }
    server.serving.coerce --> server.serving.app { RequestValidationError, bind_parameters, body_param_name, coerce_value, filter_kwargs_for_callback, get_callback_spec }
    server.serving.compression --> server.serving.server { CompressionPolicy }
    server.serving.datatypes --> client.targets.desktop.native.broker_extension { HTMLResponse, JSONResponse, Request, Response, StreamingResponse }
    server.serving.datatypes --> scale.admin.admin_portal { FileResponse, HTMLResponse, JSONResponse, RedirectResponse, Request, Response }
    server.serving.datatypes --> scale.admin.admin_portal.JacAPIServerAdmin.register_admin_endpoints { Request }
    server.serving.datatypes --> scale.admin.deploy_health { JSONResponse, Request }
    server.serving.datatypes --> scale.admin.llm_telemetry { JSONResponse, Request }
    server.serving.datatypes --> scale.admin.logs { JSONResponse, Request }
    server.serving.datatypes --> scale.admin.network { JSONResponse, Request }
    server.serving.datatypes --> scale.admin.ops { JSONResponse, Request }
    server.serving.datatypes --> scale.admin.podenv { JSONResponse, Request }
    server.serving.datatypes --> scale.admin.traces { JSONResponse, Request }
    server.serving.datatypes --> scale.admin.workloads { Request }
    server.serving.datatypes --> scale.observability.prometheus_metrics { Response }
    server.serving.datatypes --> scale.runtime.context.errors { JSONResponse }
    server.serving.datatypes --> scale.runtime.gateway.embedded_gateway { JSONResponse, Request, Response }
    server.serving.datatypes --> scale.runtime.gateway.microservice_gateway { HTMLResponse, JSONResponse, Request, Response }
    server.serving.datatypes --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.handle_admin { RedirectResponse }
    server.serving.datatypes --> scale.runtime.transport.http_forward { Response, StreamingResponse }
    server.serving.datatypes --> scale.server.extensions { JSONResponse, Request, Response }
    server.serving.datatypes --> scale.server.jobs_ext { Request }
    server.serving.datatypes --> scale.server.sso_ext { RedirectResponse, Request, Response }
    server.serving.datatypes --> scale.server.webhook_ext { Request }
    server.serving.datatypes --> scale.server.websocket_ext { WebSocketDisconnect }
    server.serving.datatypes --> scale.sso.firebase { Request, Response }
    server.serving.datatypes --> scale.sso.provider { RedirectResponse, Request, Response }
    server.serving.datatypes --> scale.sso.sso_auth { RedirectResponse, Request, Response }
    server.serving.datatypes --> scale.tests.microservices.test_drain { JSONResponse, Request, URL }
    server.serving.datatypes --> scale.tests.microservices.test_gateway { Headers, Request, URL }
    server.serving.datatypes --> scale.tests.microservices.test_gateway_webapp { JSONResponse, Request, Response }
    server.serving.datatypes --> scale.tests.microservices.test_rate_limit { Headers, Request, URL }
    server.serving.datatypes --> scale.tests.microservices.test_rate_limit.next_handler { JSONResponse }
    server.serving.datatypes --> scale.tests.server.test_bodiless_status { Response, StreamingResponse }
    server.serving.datatypes --> scale.tests.server.test_build_status_endpoint { Request }
    server.serving.datatypes --> scale.tests.server.test_firebase_auth_sso { Request }
    server.serving.datatypes --> scale.tests.server.test_oauth_providers { RedirectResponse, Request }
    server.serving.datatypes --> scale.tests.server.test_oauth_providers._callback_request { QueryParams, URL }
    server.serving.datatypes --> scale.tests.server.test_registration_limits { Request }
    server.serving.datatypes --> scale.tests.server.test_serving_tail { JSONResponse }
    server.serving.datatypes --> scale.tests.server.test_sso { Headers, QueryParams, RedirectResponse, Request, URL }
    server.serving.datatypes --> scale.tests.server.test_static_fallback { Request }
    server.serving.datatypes --> scale.tests.server.test_static_fallback._get_request { URL }
    server.serving.datatypes --> scale.tests.server.test_stream_ws { WebSocketDisconnect }
    server.serving.datatypes --> scale.tests.server.test_stream_ws._spawn_upstream { Request, Response }
    server.serving.datatypes --> scale.tests.server.test_stream_ws._spawn_upstream.big { StreamingResponse }
    server.serving.datatypes --> scale.tests.server.test_stream_ws._spawn_upstream.sse { StreamingResponse }
    server.serving.datatypes --> scale.tests.server.test_sv_streaming._StubResp.headers_obj { Headers }
    server.serving.datatypes --> scale.websocket.websocket { WebSocketDisconnect }
    server.serving.datatypes --> server.bridge.replay_response { JSONResponse }
    server.serving.datatypes --> server.bridge.serialize_response { JSONResponse }
    server.serving.datatypes --> server.endpoints.auth { Request }
    server.serving.datatypes --> server.endpoints.colocated { Request, Response }
    server.serving.datatypes --> server.endpoints.introspection { Request }
    server.serving.datatypes --> server.endpoints.pages { HTMLResponse, JSONResponse, Request, Response }
    server.serving.datatypes --> server.endpoints.walkers { Request, Response, StreamingResponse }
    server.serving.datatypes --> server.identity.audit { Request }
    server.serving.datatypes --> server.middleware { JSONResponse, Request, Response }
    server.serving.datatypes --> server.outbox.remember_response { JSONResponse }
    server.serving.datatypes --> server.serving.app { HTTPError, JSONResponse, RedirectResponse, Request, Response, StreamingResponse, parse_query_string }
    server.serving.datatypes --> server.serving.client { Headers }
    server.serving.datatypes --> server.serving.coerce { Request, UploadFile }
    server.serving.datatypes --> server.serving.compression { Headers, Request, Response }
    server.serving.datatypes --> server.serving.drain { JSONResponse, Request, Response }
    server.serving.datatypes --> server.serving.files { JSONResponse, Request, Response }
    server.serving.datatypes --> server.serving.health { JSONResponse }
    server.serving.datatypes --> server.serving.middleware { Request, Response }
    server.serving.datatypes --> server.serving.multipart { HTTPError, Request, UploadFile }
    server.serving.datatypes --> server.serving.openapi { HTMLResponse }
    server.serving.datatypes --> server.serving.proxy { Headers }
    server.serving.datatypes --> server.serving.server { Headers, QueryParams, Request, Response, URL, parse_query_string }
    server.serving.datatypes --> server.serving.server.ServingServer._dispatch { JSONResponse }
    server.serving.datatypes --> server.serving.ws { Headers, QueryParams, URL, WebSocketDisconnect }
    server.serving.datatypes --> testing.testing { Headers, QueryParams, Request, Response, URL, parse_query_string }
    server.serving.datatypes --> testing.testkit { Headers, QueryParams, Request, Response, URL, parse_query_string }
    server.serving.drain --> scale.runtime.gateway.microservice_gateway { DrainState }
    server.serving.drain --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.setup { drain_middleware }
    server.serving.drain --> scale.server.extensions { HEALTH_PATHS }
    server.serving.drain --> scale.tests.microservices.test_drain { DrainState, drain_middleware }
    server.serving.drain --> server.middleware { LIVENESS_PATHS }
    server.serving.drain --> server.server { DrainState }
    server.serving.drain --> server.server.JacAPIServer.build_app { drain_middleware }
    server.serving.drain --> server.serving.accesslog { HEALTH_PATHS }
    server.serving.drain --> server.serving.health { DrainState }
    server.serving.drain --> server.serving.server { DrainState, HEALTH_PATHS }
    server.serving.endpoint --> client.targets.desktop.native.broker_extension { APIParameter, HTTPMethod, JEndPoint, ParameterType }
    server.serving.endpoint --> scale.admin.admin_portal { APIParameter, HTTPMethod, JEndPoint, ParameterType }
    server.serving.endpoint --> scale.admin.deploy_health { HTTPMethod, JEndPoint }
    server.serving.endpoint --> scale.admin.llm_telemetry { APIParameter, HTTPMethod, JEndPoint, ParameterType }
    server.serving.endpoint --> scale.admin.logs { APIParameter, HTTPMethod, JEndPoint, ParameterType }
    server.serving.endpoint --> scale.admin.network { HTTPMethod, JEndPoint }
    server.serving.endpoint --> scale.admin.ops { APIParameter, HTTPMethod, JEndPoint, ParameterType }
    server.serving.endpoint --> scale.admin.podenv { HTTPMethod, JEndPoint }
    server.serving.endpoint --> scale.admin.traces { APIParameter, HTTPMethod, JEndPoint, ParameterType }
    server.serving.endpoint --> scale.admin.workloads { APIParameter, HTTPMethod, JEndPoint, ParameterType }
    server.serving.endpoint --> scale.runtime.gateway.microservice_gateway { JEndPoint, WSEndPoint }
    server.serving.endpoint --> scale.server.extensions { HTTPMethod, JEndPoint }
    server.serving.endpoint --> scale.server.jobs_ext { APIParameter, HTTPMethod, JEndPoint, ParameterType }
    server.serving.endpoint --> scale.server.sso_ext { APIParameter, HTTPMethod, JEndPoint, ParameterType }
    server.serving.endpoint --> scale.server.webhook_ext { APIParameter, HTTPMethod, JEndPoint, ParameterType }
    server.serving.endpoint --> scale.tests.deploy.test_ops_deploy { HTTPMethod }
    server.serving.endpoint --> scale.tests.deploy.test_ops_health { HTTPMethod }
    server.serving.endpoint --> scale.tests.deploy.test_ops_network { HTTPMethod }
    server.serving.endpoint --> scale.tests.misc.test_ops_podenv { HTTPMethod }
    server.serving.endpoint --> scale.tests.server.test_admin_logs { HTTPMethod }
    server.serving.endpoint --> scale.tests.server.test_bodiless_status { HTTPMethod, JEndPoint }
    server.serving.endpoint --> scale.tests.server.test_serving_tail { HTTPMethod, JEndPoint, WSEndPoint }
    server.serving.endpoint --> scale.tests.server.test_sso { JEndPoint }
    server.serving.endpoint --> scale.tests.server.test_stream_ws._spawn_upstream { HTTPMethod, JEndPoint }
    server.serving.endpoint --> scale.tests.server.test_stream_ws._spawn_ws_upstream { WSEndPoint }
    server.serving.endpoint --> scale.tests.server.test_stream_ws._spawn_ws_upstream_with_protocol { WSEndPoint }
    server.serving.endpoint --> scale.tests.support { JEndPoint }
    server.serving.endpoint --> server.endpoints.auth { APIParameter, HTTPMethod, JEndPoint, ParameterType }
    server.serving.endpoint --> server.endpoints.colocated { APIParameter, HTTPMethod, JEndPoint, ParameterType }
    server.serving.endpoint --> server.endpoints.introspection { APIParameter, HTTPMethod, JEndPoint, ParameterType }
    server.serving.endpoint --> server.endpoints.pages { APIParameter, HTTPMethod, JEndPoint, ParameterType }
    server.serving.endpoint --> server.endpoints.walkers { APIParameter, HTTPMethod, JEndPoint, ParameterType }
    server.serving.endpoint --> server.server { JEndPoint, WSEndPoint }
    server.serving.endpoint --> server.serving.app { JEndPoint, WSEndPoint }
    server.serving.endpoint --> server.serving.coerce { APIParameter, JEndPoint, ParameterType }
    server.serving.endpoint --> server.serving.health { HTTPMethod, JEndPoint }
    server.serving.endpoint --> server.serving.openapi { APIParameter, HTTPMethod, JEndPoint, ParameterType }
    server.serving.endpoint --> server.serving.router { HTTPMethod, JEndPoint, WSEndPoint }
    server.serving.executor --> server.serving.server { SyncExecutor }
    server.serving.files --> server.endpoints.pages { file_response }
    server.serving.health --> server.server.JacAPIServer.register_endpoints { register_health_endpoints }
    server.serving.middleware --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.setup { cors_middleware }
    server.serving.middleware --> server.server.JacAPIServer.build_app { cors_middleware, custom_headers_middleware }
    server.serving.model --> scale.scheduler.scheduler_models { ApiModel, require_str }
    server.serving.model --> server.identity.auth_models { ApiModel, require_str }
    server.serving.multipart --> server.serving.app { parse_multipart, parse_urlencoded_form }
    server.serving.openapi --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.handle_docs { swagger_ui_html }
    server.serving.openapi --> scale.tests.server.test_serving_tail { build_openapi }
    server.serving.openapi --> server.server.JacAPIServer._refresh_dev_endpoints { register_docs_endpoints }
    server.serving.openapi --> server.server.JacAPIServer.build_app { register_docs_endpoints }
    server.serving.openapi --> server.serving.app.ServingApp.openapi { build_openapi }
    server.serving.proxy --> scale.tests.microservices.test_rate_limit { ProxyResolver, _untrusted_warned, logger as _proxy_logger }
    server.serving.proxy --> server.serving.server { ProxyResolver }
    server.serving.router --> server.endpoints.walkers { path_param_names }
    server.serving.router --> server.serving.app { Router }
    server.serving.server --> scale.runtime.gateway.embedded_gateway.EmbeddedGateway.serve { PORT_RETRY_LIMIT, ServingServer }
    server.serving.server --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.start { ServingServer }
    server.serving.server --> scale.tests.microservices.test_app_routes._expose_backend { ServingServer }
    server.serving.server --> scale.tests.microservices.test_drain { ServingServer }
    server.serving.server --> scale.tests.microservices.test_gateway_webapp { ServingServer }
    server.serving.server --> scale.tests.microservices.test_microservice { ServingServer }
    server.serving.server --> scale.tests.server.test_bodiless_status { ServingServer }
    server.serving.server --> scale.tests.server.test_serving_tail { ServingServer }
    server.serving.server --> scale.tests.server.test_stream_ws._spawn_upstream { ServingServer }
    server.serving.server --> scale.tests.server.test_stream_ws._spawn_ws_upstream { ServingServer }
    server.serving.server --> scale.tests.server.test_stream_ws._spawn_ws_upstream_with_protocol { ServingServer }
    server.serving.server --> scale.tests.server.test_sv_outbox_endpoints { ServingServer }
    server.serving.server --> server.server { ServingServer }
    server.serving.server --> server.serving.supervisor { EXIT_OK, EXIT_RECYCLE }
    server.serving.server --> testing.testkit { ServingServer }
    server.serving.sse --> scale.runtime.rpc.rpc._iter_sse_text { consume_sse_events }
    server.serving.sse --> scale.tests.microservices.test_sse_framing { sse_frame_stream }
    server.serving.sse --> scale.tests.server.test_sv_streaming { consume_sse_events as consume_sse_stream, parse_sse as _parse_sse }
    server.serving.sse --> server.endpoints.walkers { sse_frame_stream }
    server.serving.sse --> server.serving.app { sse_frame_stream }
    server.serving.sse --> server.serving.client { parse_sse }
    server.serving.sse --> server.sv_client._http_call { consume_sse_events }
    server.serving.supervisor --> cli.commands.execution.serve { worker_metrics_dir }
    server.serving.supervisor --> runtime.source_app.main { worker_metrics_dir }
    server.serving.supervisor --> server.server { WorkerHandle }
    server.serving.supervisor --> server.server.JacAPIServer.start { WorkerSupervisor }
    server.serving.ws --> scale.runtime.gateway.microservice_gateway { WebSocket }
    server.serving.ws --> scale.server.websocket_ext { WebSocket }
    server.serving.ws --> scale.tests.server.test_serving_tail { OP_CLOSE, OP_CONT, OP_PING, OP_PONG, OP_TEXT, encode_frame, read_frame }
    server.serving.ws --> scale.websocket.protocol { WebSocket }
    server.serving.ws --> scale.websocket.websocket { WebSocket }
    server.serving.ws --> server.serving.client { WebSocket, compute_accept_key }
    server.serving.ws --> server.serving.server { WebSocket, compute_accept_key }
    server.serving.authcrypt --> scale.tests.deploy.test_pod_env { PLACEHOLDER_JWT_SECRET }
    server.serving.drain --> server.task_scheduler { DrainState }
    server.serving.app --> server.exchange.settle_envelope { transport_to_response }
    server.serving.authcrypt --> scale.tests.deploy.test_deployment_overlay { PLACEHOLDER_JWT_SECRET }
    server.serving.authcrypt --> scale.tests.server.test_admin { jwt_decode }
    server.serving.authcrypt --> server.identity.assurance { jwt_decode }
    server.serving.client --> scale.tests.server.test_serve { run_blocking }
    server.serving.datatypes --> scale.tests.data.test_gateway_owned_identity { Request, Response }
    server.serving.datatypes --> scale.tests.server.test_serve { Headers, Request, URL }
    server.serving.datatypes --> server.endpoints.second_factor { Request }
    server.serving.datatypes --> server.endpoints.walkers { FileResponse }
    server.serving.datatypes --> server.exchange { JSONResponse, Request }
    server.serving.datatypes --> server.identity.session_cookie { Request, Response }
    server.serving.endpoint --> server.endpoints.second_factor { HTTPMethod, JEndPoint }
    server.serving.files --> server.endpoints.walkers { file_response }
    server.serving.app --> scale.tests.microservices.test_sse_framing { ServingApp }
    server.serving.app --> scale.tests.server.test_auth_policy_startup { transport_to_response }
    server.serving.authcrypt --> scale.deploy.target.kubernetes.manifest_builder { PLACEHOLDER_JWT_SECRET }
    server.serving.authcrypt --> scale.deploy.target.kubernetes.utils.kubernetes_utils.resolve_minted_secret { PLACEHOLDER_JWT_SECRET }
    server.serving.client --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.forward_to { ClientReadTimeout }
    server.serving.client --> scale.runtime.gateway.microservice_gateway.MicroserviceGateway.probe_services { ClientReadTimeout }
    server.serving.client --> scale.runtime.transport.http_forward { ClientReadTimeout }
    server.serving.client --> server.identity.policy { request_sync }
    server.serving.compression --> scale.tests.microservices.test_sse_framing { _gzip_stream }
    server.serving.endpoint --> scale.tests.server.test_auth_policy_startup { JEndPoint }
    server.serving.endpoint --> server.server.restspec_fields { HTTPMethod }
    server.serving.executor --> server.serving.compression { iterate_sync }
    server.serving.executor --> server.serving.server { iterate_sync }
    server.serving.executor --> server.serving.sse { iterate_sync }
    server.serving.server --> scale.tests.microservices.test_sse_framing { ServingServer }
    testing.cl_test_runner --> scale.tests.server.test_cl_test_runner { run_cl_test_file }
    testing.cl_test_runner --> testing.runner.run_test { is_cl_test_file, is_cl_test_file_for_discovery, register_results_into_jactestcheck, run_cl_test_file }
    testing.cl_test_runner --> testing.test_runner.run_file { module_is_client, run_cl_test_file }
    testing.requires --> byllm.tests.test_media { require_module }
    testing.requires --> scale.tests.deploy.test_deploy_k8s { require_flag }
    testing.requires --> scale.tests.microservices.test_fat_bundle { require_network }
    testing.requires --> scale.tests.server.test_scheduler_endpoints { require_module }
    testing.requires --> scale.tests.server.test_scheduler_multipod { require_module }
    testing.runner --> compiler.driver.build_services.CompilerBuildServices.run_test { run_test }
    testing.test --> compiler.tests.test_pipeline_products { parametrize }
    testing.test --> compiler.tests.test_prim_equivalence { parametrize }
    testing.test --> runtime.runtime.JacTest.jac_test { JacTestCheck }
    testing.test --> scale.tests.deploy.test_k8s_utils { parametrize }
    testing.test --> testing.cl_test_runner.register_results_into_jactestcheck { JacTestCheck }
    testing.test --> testing.runner.run_test { JacTestCheck }
    testing.test --> testing.test_runner.run_file { JacTestCheck }
    testing.test_runner --> byllm.tests.support.need_outside_jaclang { strict_mode }
    testing.test_runner --> cli.commands.analysis.test { run_tests }
    testing.test_runner --> scale.tests.support { STRICT_ENV, strict_mode }
    testing.test_runner --> testing.requires { STRICT_ENV, strict_mode }
    testing.testkit --> scale.server.inprocess.prepare_inprocess_runtime { ServingTestClient }
    testing.testkit --> scale.tests.apps.test_fleet_from_apps { ServingTestClient as TestClient }
    testing.testkit --> scale.tests.data.test_eager_spawn { ServingTestClient as TestClient }
    testing.testkit --> scale.tests.microservices.test_app_routes { ServingTestClient as TestClient }
    testing.testkit --> scale.tests.microservices.test_embedded_gateway { ServingTestClient as TestClient }
    testing.testkit --> scale.tests.microservices.test_gateway { ServingTestClient as TestClient }
    testing.testkit --> scale.tests.microservices.test_gateway._gateway { ServingTestClient as TestClient }
    testing.testkit --> scale.tests.microservices.test_gateway_docs_precedence { ServingTestClient }
    testing.testkit --> scale.tests.microservices.test_gateway_webapp { ServingTestClient }
    testing.testkit --> scale.tests.microservices.test_microservice { ServingTestClient as TestClient }
    testing.testkit --> scale.tests.server.test_served_app_route { ServingTestClient as TestClient }
    testing.testkit --> scale.tests.server.test_stream_ws { ServingTestClient as TestClient }
    testing.testkit --> scale.tests.server.test_sv_outbox_endpoints { ServingTestClient as TestClient }
    testing.testkit --> testing.testing { dispatch_and_collect }
    testing.requires --> byllm.tests.test_timeout { require_module }
    toolchains.android --> client.targets.react_native.build.run_eas_local_build { ensure_android }
    toolchains.android --> client.targets.react_native.build.run_gradle_assemble { ensure_android }
    toolchains.android --> toolchains.manager.setup_toolchain { ensure_android }
    toolchains.apple --> client.targets.react_native.build.run_eas_local_build { ensure_apple }
    toolchains.apple --> client.targets.react_native.build.run_xcodebuild_ios { ensure_apple }
    toolchains.apple --> toolchains.manager.setup_toolchain { ensure_apple }
    toolchains.c_backend --> compiler.backends.native.c_emit.emit_c { ensure_c_backend }
    toolchains.c_backend --> dist.source.project.export_project { c_backend_license, c_backend_provenance }
    toolchains.cef --> client.targets.desktop.cef_shell { ensure_cef }
    toolchains.cef --> toolchains.manager.setup_toolchain { ensure_cef }
    toolchains.desktop --> client.targets.desktop.desktop_build._find_cef_dir { source_workspace }
    toolchains.desktop --> client.targets.desktop.desktop_build._find_native_asset_dir { source_workspace }
    toolchains.desktop --> client.targets.desktop.desktop_build._find_webview_dir { source_workspace }
    toolchains.desktop --> client.targets.desktop.desktop_build.build_cef_dispatch { source_workspace }
    toolchains.desktop --> client.targets.desktop.desktop_build.build_cef_subprocess { source_workspace }
    toolchains.desktop --> client.targets.desktop.macos_bundle { MACOS_DESKTOP_MIN_VERSION }
    toolchains.desktop --> client.targets.desktop.webview_shell { ensure_webview, webview_library_name }
    toolchains.desktop --> toolchains.manager.setup_toolchain { ensure_webview }
    toolchains.host --> client.targets.desktop.webview_shell { host_platform }
    toolchains.host --> client.targets.react_native.build.run_xcodebuild_ios { run_step }
    toolchains.host --> toolchains.android { executable, host_platform, run_step }
    toolchains.host --> toolchains.apple { host_platform, run_step, use_system_tools }
    toolchains.host --> toolchains.c_backend { executable, host_platform, run_step }
    toolchains.host --> toolchains.cef { host_platform }
    toolchains.host --> toolchains.desktop { host_platform, run_step, shared_library_name }
    toolchains.host --> toolchains.system { run_step }
    toolchains.host --> toolchains.system.ensure_desktop_host { host_platform }
    toolchains.host --> toolchains.system.ensure_linux_desktop { host_platform }
    toolchains.javascript --> client.targets.react_native.build.run_eas_local_build { build_environment }
    toolchains.javascript --> client.targets.react_native.build.run_expo_prebuild { build_environment }
    toolchains.javascript --> client.targets.react_native.build.run_gradle_assemble { build_environment }
    toolchains.javascript --> client.targets.react_native.build.run_xcodebuild_ios { build_environment }
    toolchains.javascript --> toolchains.manager.setup_toolchain { native_node }
    toolchains.manager --> client.cli.setup { setup_toolchain }
    toolchains.pins --> toolchains.android { ANDROID_ARTIFACTS }
    toolchains.pins --> toolchains.apple.ensure_apple { RUBY_ARTIFACTS, RUBY_VERSION }
    toolchains.store --> client.targets.mobile_target.MobileTarget.ensure_ready { offline }
    toolchains.store --> client.targets.node_tooling_common.run_manifest_install { offline }
    toolchains.store --> client.targets.react_native.build.run_eas_local_build { offline }
    toolchains.store --> client.targets.react_native.build.run_gradle_assemble { offline }
    toolchains.store --> client.targets.react_native.build.run_xcodebuild_ios { offline }
    toolchains.store --> scale.injector.binary._fetch_verified_asset { Artifact, fetch }
    toolchains.store --> toolchains.android { install, offline }
    toolchains.store --> toolchains.apple { install_slot, offline, publish_install_slot, slot_installed }
    toolchains.store --> toolchains.apple.ensure_apple { install }
    toolchains.store --> toolchains.c_backend { Artifact, build_slot, extract, fetch, file_digest, publish_build_slot, slot_ready }
    toolchains.store --> toolchains.cef { Artifact, install }
    toolchains.store --> toolchains.desktop { Artifact, build_slot, fetch, file_digest, publish_build_slot, slot_ready }
    toolchains.store --> toolchains.javascript { offline }
    toolchains.store --> toolchains.pins { Artifact }
    toolchains.store --> toolchains.system { offline }
    toolchains.system --> client.targets.desktop.desktop_build._patchelf_rpath { ensure_patchelf }
    toolchains.system --> toolchains.desktop { ensure_desktop_host, webkit_module }
    toolchains.store --> packages.index.Registry._read { allowed_url, offline }
    toolchains.store --> packages.index.fetch_verified { Artifact, fetch }
    toolchains.store --> packages.sources.checkout { offline }
    toolchains.host --> toolchains.tools { executable, host_platform, use_system_tools }
    toolchains.pins --> toolchains.tools.JdkArtifact._home { JDK_VERSION }
    toolchains.pins --> toolchains.tools.JdkArtifact.pinned { JDK_ARTIFACTS }
    toolchains.pins --> toolchains.tools.NodeArtifact.pinned { NODE_ARTIFACTS }
    toolchains.pins --> toolchains.tools.PatchelfArtifact.pinned { PATCHELF_ARTIFACTS }
    toolchains.store --> data.pg_dist._unpack { Artifact as Download, extract, fetch }
    toolchains.store --> toolchains.tools { Artifact as Download, install, installed }
    toolchains.tools --> toolchains.android.ensure_jdk { tool_path }
    toolchains.tools --> toolchains.javascript.native_node { tool_path }
    toolchains.tools --> toolchains.system.ensure_patchelf { tool_path }
    packages.api --> packages.artifact.build_package { package_surface }
    packages.api --> packages.artifact.package_manifest { surface_digest }
    packages.api --> packages.verify._verify_library { package_surface, surface_digest }
    packages.apidiff --> packages.publish { ApiChange, check_bump, diff_surfaces, minimum_next }
    packages.apidiff --> packages.verify { check_bump, diff_surfaces }
    packages.artifact --> cli.commands.project._bundle_jab { ArtifactError, ROLE_APP, build_package, project_role }
    packages.artifact --> dist.seal.vendor_packages { stage_source_tree }
    packages.artifact --> packages.commands._dep_from_source { read_identity }
    packages.artifact --> packages.publish { API_FILE, ArtifactError, BuiltPackage, MANIFEST_DIR, ROLE_LIB, ROLE_TEMPLATE, build_package, package_identity, project_role }
    packages.artifact --> packages.sources { pack_source_tree }
    packages.artifact --> packages.store { ArtifactError, expect_identity }
    packages.artifact --> packages.templates { MANIFEST_DIR, ROLE_TEMPLATE, read_package_manifest }
    packages.artifact --> packages.verify { API_FILE, MANIFEST_DIR, read_package_manifest }
    packages.commands --> cli.commands.project.install { add_packages, install_project }
    packages.commands --> cli.commands.project.remove { remove_packages }
    packages.commands --> cli.commands.project.update { PYPI_HINT, install_project, split_package_specs }
    packages.github --> packages.index._github_tree { find_token }
    packages.github --> packages.publish.open_index_pull { GitHub }
    packages.index --> packages.install { RegistryError, registry_named }
    packages.index --> packages.install._registry_for_source { Registry, registry_urls }
    packages.index --> packages.publish { IndexEntry, Registry, RegistryError, api_rel_path, index_rel_path, parse_index_lines, registry_named }
    packages.index --> packages.resolve { IndexEntry, Registry, RegistryError, registry_named, registry_urls }
    packages.index --> packages.templates { IndexEntry, RegistryError, registry_named }
    packages.index --> packages.verify { API_DIR, IndexEntry, Registry, RegistryError, api_rel_path, fetch_verified, parse_index_lines }
    packages.install --> client.config_loader._package_npm_deps { InstallError, load_lock, package_npm_requirements }
    packages.install --> dist.seal.vendor_packages { has_packages, sync }
    packages.install --> packages.commands { InstallError, SyncResult, describe_sync, has_packages, load_lock, project_dir, sync, write_lock }
    packages.install --> packages.provider { InstallError, load_lock, package_npm_requirements, package_pip_requirements }
    packages.install --> packages.verify._verify_library { InstallError, sync }
    packages.lock --> packages.commands { Lockfile, digest_of }
    packages.lock --> packages.install { LockError, LockedPackage, Lockfile }
    packages.lock --> packages.resolve { LockedPackage, Lockfile, digest_of }
    packages.migrate --> cli.commands.fix._fix_dependencies { find_manifests, migrate_manifest }
    packages.mounts --> packages.install { link_mounts }
    packages.provider --> project.providers.initialize_provider_registry { JacPackageProvider }
    packages.pubgrub --> packages.resolve { PackageSource, SolveFailure, solve }
    packages.publish --> cli.commands.project.publish { publish_project, yank_version }
    packages.publish --> packages.verify { previous_release, previous_surface }
    packages.resolve --> packages.artifact.package_manifest { manifest_npm, manifest_pypi }
    packages.resolve --> packages.commands { manifest_inputs }
    packages.resolve --> packages.install { ResolveError, manifest_inputs, pip_requirement, resolve_graph }
    packages.resolve --> packages.templates { running_jac_version }
    packages.semver --> packages.apidiff { Version }
    packages.semver --> packages.commands { SemverError, Version, caret_for }
    packages.semver --> packages.commands.add_packages { Requirement }
    packages.semver --> packages.pubgrub { Requirement, Version, VersionSet }
    packages.semver --> packages.publish | packages.verify { SemverError, Version }
    packages.semver --> packages.resolve | packages.templates { Requirement, SemverError, Version }
    packages.sources --> packages.commands._dep_from_source { checkout, resolve_path }
    packages.sources --> packages.install { GitError, checkout, pack_checkout }
    packages.sources --> packages.resolve { GitError, checkout, pack_checkout, resolve_path }
    packages.store --> packages.install { StoreError, cached, materialize }
    packages.templates --> cli.commands.project._resolve_template { TemplateError, fetch_template, is_template_spec, load_template_jab }
    packages.verify --> cli.commands.project.publish { run_verify }
    artifacts.kit --> artifacts.router._omitted { kit_image }
    artifacts.kit --> client.js_runtime.BunArtifact.build { osarch }
    artifacts.kit --> client.js_runtime.BunArtifact.probe_kit { kit_image }
    artifacts.kit --> compiler.backends.native.floors { osarch, runtime_floor_root }
    artifacts.kit --> compiler.backends.native.kernel_resolve._bundled_kernel { kit_image }
    artifacts.kit --> compiler.backends.native.link_plan.link_artifact { osarch }
    artifacts.kit --> compiler.backends.native.llvm.shim_path.ShimArtifact.probe_kit { kit_image, kit_path }
    artifacts.kit --> compiler.backends.native.static_link.floor_lib_dir { osarch }
    artifacts.kit --> compiler.backends.native.static_link.musl_lib_dir { osarch }
    artifacts.kit --> compiler.types.stubcat.locate.StubcatArtifact.probe_kit { kit_image, kit_path }
    artifacts.kit --> dist.interpreter.JacPythonArtifact.probe_kit { kit_image }
    artifacts.kit --> dist.precompile_bytecode.kit_omissions { pr_kit_omits }
    artifacts.model --> artifacts.router { Artifact, ArtifactKind, ArtifactUnavailable, Probe, ReleasePolicy, Resolution, Source }
    artifacts.model --> cli.commands.execution._run_node_tool { ArtifactUnavailable }
    artifacts.model --> cli.commands.native { ArtifactUnavailable, Probe }
    artifacts.model --> client.cli.run_npm_add_global { ArtifactUnavailable }
    artifacts.model --> client.js_runtime { Artifact, ArtifactKind, Probe, ReleasePolicy, Source }
    artifacts.model --> compiler.backends.native.floors { Artifact, ArtifactKind, Probe, ReleasePolicy, Source }
    artifacts.model --> compiler.backends.native.kernel_resolve { Artifact, ArtifactKind, Probe, ReleasePolicy, Source }
    artifacts.model --> compiler.backends.native.llvm.binding.ffi { ArtifactUnavailable }
    artifacts.model --> compiler.backends.native.llvm.shim_path { Artifact, ArtifactKind, Probe, ReleasePolicy, Source }
    artifacts.model --> compiler.tests.test_stubcat_roundtrip { Probe, Source }
    artifacts.model --> compiler.types.stubcat.locate { Artifact, ArtifactKind, Probe, ReleasePolicy, Source }
    artifacts.model --> data.pg_dist { Artifact, ArtifactKind, ArtifactUnavailable, Probe, ReleasePolicy, Source }
    artifacts.model --> dist.interpreter { Artifact, ArtifactKind, Probe, ReleasePolicy, Source }
    artifacts.model --> dist.payload.fetch.fetch_bun { Source }
    artifacts.model --> dist.precompiled { Artifact, ArtifactKind, Probe, ReleasePolicy, Source }
    artifacts.model --> dist.seal.ensure_client_dist { ArtifactUnavailable }
    artifacts.model --> project.compiler_host.ProjectHost.typeshed_unavailable_reason { ArtifactUnavailable }
    artifacts.model --> server.server { ArtifactUnavailable }
    artifacts.model --> toolchains.c_backend { Artifact as ArtifactBase, ArtifactKind, Probe, ReleasePolicy, Source }
    artifacts.model --> toolchains.tools { Artifact, ArtifactKind, ArtifactUnavailable, Probe, ReleasePolicy, Source }
    artifacts.router --> artifacts.model.Artifact.disabled { building_now }
    artifacts.router as router --> cli.commands.native | compiler.tests.test_stubcat_roundtrip;
    artifacts.router --> client.js_engine.engine_dir { require }
    artifacts.router --> client.js_runtime.JsEngineArtifact.floor_present { resolve }
    artifacts.router --> client.js_runtime.JsEngineArtifact.provide_floor { build }
    artifacts.router --> client.js_runtime._engine { resolve }
    artifacts.router --> client.js_runtime.js_runtime_path { require }
    artifacts.router --> compiler.backends.native.kernel_resolve.build_kernel { publish }
    artifacts.router --> compiler.backends.native.kernel_resolve.resolve_kernel { resolve }
    artifacts.router --> compiler.backends.native.llvm.shim_path.shim_path { require }
    artifacts.router --> compiler.backends.native.static_link.floor_lib_dir { resolve }
    artifacts.router --> compiler.backends.native.static_link.musl_lib_dir { resolve }
    artifacts.router --> compiler.backends.native.wasm_build._link_wasm_libc { require }
    artifacts.router --> compiler.backends.native.wasm_build._wasm_libc_dir { resolve }
    artifacts.router --> compiler.driver.toolchain.native_pipeline_available { resolve }
    artifacts.router --> compiler.types.stubcat.build.build_catalog { building }
    artifacts.router --> compiler.types.stubcat.locate.open_catalog { resolve }
    artifacts.router --> data.pg_dist.postgres_bin_dir { require }
    artifacts.router --> project.compiler_host.ProjectHost.typeshed_unavailable_reason { require }
    artifacts.router --> project.kernel_snapshot.build_stub_catalog { artifact_named, build, forget }
    artifacts.router --> project.kernel_snapshot.catalog_build_blocker { artifact_named }
    artifacts.router --> project.kernel_snapshot.require_stub_catalog { forget }
    artifacts.router --> toolchains.c_backend.ensure_c_backend { require }
    artifacts.router --> toolchains.tools.tool_path { require }
    runtime.na_stdlib._bz2_native --> runtime.na_stdlib.bz2 { bz2_compress, bz2_decompress }
    runtime.na_stdlib._csprng_native --> runtime.na_stdlib.secrets { csprng_bytes }
    runtime.na_stdlib._csprng_native --> runtime.na_stdlib.uuid { csprng_bytes }
    runtime.na_stdlib._datetime_native --> runtime.na_stdlib.datetime { dt_epoch_us, dt_fmt_buf, dt_gmtime, dt_localtime, dt_out_buf, dt_out_str, dt_strftime, dt_tm, dt_tm_gmtoff, dt_tm_zone }
    runtime.na_stdlib._directory_native --> runtime.na_stdlib.glob { try_directory_names }
    runtime.na_stdlib._directory_native --> runtime.na_stdlib.pathlib { directory_names }
    runtime.na_stdlib._directory_native --> runtime.na_stdlib.shutil { try_directory_names }
    runtime.na_stdlib._directory_native --> runtime.na_stdlib.uuid { try_directory_names }
    runtime.na_stdlib._directory_native --> runtime.na_stdlib.zoneinfo { try_directory_names }
    runtime.na_stdlib._dirent_native --> runtime.na_stdlib._directory_native { dirent_name }
    runtime.na_stdlib._errno_native --> runtime.na_stdlib._datetime_native { last_errno, raise_os_error }
    runtime.na_stdlib._errno_native --> runtime.na_stdlib._directory_native { clear_errno, last_errno, raise_os_error }
    runtime.na_stdlib._errno_native --> runtime.na_stdlib._file_native { last_errno, raise_os_error }
    runtime.na_stdlib._errno_native --> runtime.na_stdlib._replace_native { last_errno, raise_os_error }
    runtime.na_stdlib._errno_native --> runtime.na_stdlib._socket_native { errno_message }
    runtime.na_stdlib._errno_native --> runtime.na_stdlib._time_common { last_errno, raise_errno }
    runtime.na_stdlib._errno_native --> runtime.na_stdlib.shutil { errno_message }
    runtime.na_stdlib._errno_native --> runtime.na_stdlib.socket { errno_message }
    runtime.na_stdlib._errno_platform --> runtime.na_stdlib._errno_native { errno_address }
    runtime.na_stdlib._file_native --> runtime.na_stdlib.gettext { read_file_bytes }
    runtime.na_stdlib._file_native --> runtime.na_stdlib.io { close_stream, open_stream, read_stream, read_stream_all, seek_stream }
    runtime.na_stdlib._file_native --> runtime.na_stdlib.mimetypes { read_file_bytes }
    runtime.na_stdlib._file_native --> runtime.na_stdlib.pathlib { read_file_bytes }
    runtime.na_stdlib._file_native --> runtime.na_stdlib.uuid { read_file_bytes }
    runtime.na_stdlib._file_native --> runtime.na_stdlib.zoneinfo { read_file_bytes }
    runtime.na_stdlib._glob_native --> runtime.na_stdlib.glob { glob_lexists }
    runtime.na_stdlib._hashlib_native --> runtime.na_stdlib.hashlib { block_size_for, ctx_require, digest_size_for, evp_ctx_clone, evp_ctx_digest, evp_ctx_free, evp_ctx_new, evp_ctx_update, evp_md_for }
    runtime.na_stdlib._hashlib_native --> runtime.na_stdlib.hmac { block_size_for, ctx_require, digest_size_for, evp_md_for, hmac_ctx_clone, hmac_ctx_digest, hmac_ctx_free, hmac_ctx_new, hmac_ctx_update }
    runtime.na_stdlib._hex --> runtime.na_stdlib.hashlib { to_hex }
    runtime.na_stdlib._hex --> runtime.na_stdlib.hmac { to_hex }
    runtime.na_stdlib._hex --> runtime.na_stdlib.secrets { to_hex }
    runtime.na_stdlib._locale_tables --> runtime.na_stdlib.locale { _load_alias, _load_encalias }
    runtime.na_stdlib._logging_native --> runtime.na_stdlib.logging { log_fclose, log_fflush, log_fopen, log_fputs, log_strftime }
    runtime.na_stdlib._math_fused --> runtime.na_stdlib.math { fmadd }
    runtime.na_stdlib._math_native --> runtime.na_stdlib.cmath { m_asinh, m_atan2, m_copysign, m_cos, m_cosh, m_exp, m_fabs, m_hypot, m_log, m_log1p, m_sin, m_sinh, m_sqrt, m_tan, m_tanh }
    runtime.na_stdlib._math_native --> runtime.na_stdlib.math { m_acos, m_acosh, m_asin, m_asinh, m_atan, m_atan2, m_atanh, m_cbrt, m_ceil, m_copysign, m_cos, m_cosh, m_erf, m_erfc, m_exp, m_exp2, m_expm1, m_fabs, m_floor, m_fma, m_fmod, m_log, m_log10, m_log1p, m_log2, m_pow, m_remainder, m_sin, m_sinh, m_sqrt, m_tan, m_tanh, m_trunc }
    runtime.na_stdlib._mimetypes_tables --> runtime.na_stdlib.mimetypes { _default_common_ext, _default_common_val, _default_encodings_map, _default_knownfiles, _default_suffix_map, _default_types_ext, _default_types_val }
    runtime.na_stdlib._passwd_layout --> runtime.na_stdlib._user_home { PASSWD_DIR, PASSWD_SIZE }
    runtime.na_stdlib._replace_native --> runtime.na_stdlib._os_native { replace_file }
    runtime.na_stdlib._socket_abi --> runtime.na_stdlib._socket_native { ADDRINFO_ADDRLEN_OFFSET, ADDRINFO_ADDR_OFFSET, ADDRINFO_NEXT_OFFSET, ADDRINFO_SIZE }
    runtime.na_stdlib._socket_abi --> runtime.na_stdlib.socket { IPV6_FAMILY, address_family }
    runtime.na_stdlib._socket_native --> runtime.na_stdlib.socket { gai_str, resolve_all, sock_close, sock_connect, sock_open, sock_recv, sock_send }
    runtime.na_stdlib._sqlite3_native --> runtime.na_stdlib.sqlite3 { sq3_bind_blob, sq3_bind_double, sq3_bind_int, sq3_bind_null, sq3_bind_parameter_count, sq3_bind_parameter_name, sq3_bind_seq, sq3_bind_text, sq3_busy_timeout, sq3_changes, sq3_clear_bindings, sq3_close, sq3_column_count, sq3_column_name, sq3_complete, sq3_errmsg, sq3_exec, sq3_exec_err, sq3_finalize, sq3_free, sq3_get_autocommit, sq3_last_insert_rowid, sq3_libversion, sq3_open_err, sq3_open_v2, sq3_prep_sqlp, sq3_prep_stmt, sq3_prepare, sq3_reset, sq3_row, sq3_step, sq3_tail_nonws, sq3_total_changes }
    runtime.na_stdlib._ssl_native --> runtime.na_stdlib.ssl { ctx_free, ctx_load_ca_file, ctx_load_default_ca, ctx_new_verifying, do_handshake, last_error, ssl_close, ssl_new_client, ssl_read, ssl_write_all, verify_message, verify_result }
    runtime.na_stdlib._tarfile_native --> runtime.na_stdlib.tarfile { tar_chmod, tar_close, tar_create, tar_link, tar_read_file, tar_symlink, tar_utime, tar_write }
    runtime.na_stdlib._time_common --> runtime.na_stdlib._datetime_native { time_clock_ns }
    runtime.na_stdlib._time_common --> runtime.na_stdlib.time { time_clock_ns, time_clock_seconds, time_clock_set_ns }
    runtime.na_stdlib._typename --> runtime.na_stdlib.hmac | runtime.na_stdlib.secrets { typename }
    runtime.na_stdlib._user_home --> runtime.na_stdlib.os.path { user_home }
    runtime.na_stdlib._zlib_native --> runtime.na_stdlib.gzip { ZInflateResult, Z_MEM_ERROR, Z_OK, Z_STREAM_END, z_compress2, z_compress_bound, z_crc32, z_inflate_all, z_inflate_bound }
    runtime.na_stdlib._zlib_native --> runtime.na_stdlib.zipfile { ZInflateResult, Z_MEM_ERROR, Z_STREAM_END, z_crc32, z_inflate_all, z_inflate_bound }
    runtime.na_stdlib._zlib_native --> runtime.na_stdlib.zlib { ZInflateResult, Z_MEM_ERROR, Z_OK, Z_STREAM_END, z_adler32, z_compress2, z_compress_bound, z_crc32, z_inflate_all, z_inflate_bound }
    runtime.na_stdlib._zstd_native --> runtime.na_stdlib.compression.zstd { ZSTD_C_COMPRESSION_LEVEL, ZSTD_D_WINDOW_LOG_MAX, zstd_cctx_free, zstd_cctx_new, zstd_cctx_set, zstd_compress2, zstd_compress_bound, zstd_dctx_free, zstd_dctx_new, zstd_dctx_set, zstd_decompress_stream, zstd_error_name, zstd_frame_content_size, zstd_frame_dict_id, zstd_is_error, zstd_version_number }
    runtime.na_stdlib.datetime --> runtime.na_stdlib.zoneinfo { _MAXORDINAL, _ord2ymd }
    runtime.na_stdlib.http.client --> runtime.na_stdlib.urllib.request { HTTPResponse }
}
