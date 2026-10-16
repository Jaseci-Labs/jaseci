graph import {
    edge CoreInternal: core.* --> core.*;
    edge AppOverCore: core.* --> web.* | mobile.* | cli.* | desktop.*;
    edge WebInternal: web.* --> web.*;
    edge MobileInternal: mobile.* --> mobile.*;
    edge CliInternal: cli.* --> cli.*;
    edge DesktopInternal: desktop.* --> desktop.*;
    edge SsoFunnel: jaclang.scale.sso.* --> core.jacyac.github.auth;
    edge BridgeFunnel: jaclang.server.bridge --> cli.commands.*;
    cli.commands.common --> cli.commands.docs { EXIT_OK, explain_bridge_error }
    cli.commands.common --> cli.commands.feed { EXIT_OK, EXIT_REJECTED, EXIT_USAGE, explain_bridge_error, warn }
    cli.commands.common --> cli.commands.score { EXIT_FAILURE, EXIT_OK, EXIT_USAGE, warn }
    cli.commands.common --> cli.main { EXIT_USAGE, warn }
    cli.commands.docs --> cli.main { run_docs }
    cli.commands.feed --> cli.main { run_feed, run_post }
    cli.commands.score --> cli.main { run_score }
    core.ai --> cli.commands.score | core.scoring_service { optional_review }
    core.ai --> core.leaderboard.scoring { CodeReview }
    core.async_utils --> core.jacyac.registration | core.site.docs.DocsShell { sleep }
    core.github --> cli.commands.score { RepoMeta, code_breakdown, download_tarball, head_sha, mb_of, repo_meta, text_of, untar }
    core.github --> core.install | core.jacyac.github.repos { fetch }
    core.github --> core.leaderboard.scoring { RepoMeta }
    core.github --> core.packages.catalog { API_ROOT, fetch, parse_repo_url }
    core.github --> core.scoring_service { RepoMeta, code_breakdown, download_tarball, head_sha, repo_meta, text_of, untar }
    core.github --> core.social_graph | core.leaderboard.board { parse_repo_url }
    core.github_contracts --> core.github { GithubCommit, GithubRepository }
    core.github_contracts --> core.jacyac.github.repos { GithubRepository, GithubUser }
    core.install --> core.site.ui.Navbar { ensure_install }
    core.install --> web.main { ensure_install, install_sh }
    core.jac_tokenizer --> core.site.ui.CodeBlock { Token, tokenize_lines }
    core.scoring_service --> core.social_graph { ScoredPayload, fetch_and_score }
    core.social_graph --> cli.commands.feed { create_tweet, load_feed }
    core.social_graph --> core.jacyac.native.components.TweetCard { Tweet }
    core.social_graph --> core.jacyac.native.screens.ChannelsScreen { ChannelBundle, Tweet }
    core.social_graph --> core.jacyac.native.screens.ExploreScreen { Profile, TrendingTag }
    core.social_graph --> core.jacyac.native.screens.FeedScreen { Tweet }
    core.social_graph --> core.jacyac.native.screens.ProfileScreen { ProfileBundle }
    core.social_graph --> core.jacyac.scores { Project }
    core.social_graph --> core.jacyac.state { ChannelBundle, Profile, ProfileBundle, Project, TrendingTag, Tweet, add_comment, add_project, clear_avatar, create_channel, create_channel_tweet, create_tweet, delete_tweet, follow_user, get_all_profiles, get_all_projects, get_avatars, get_channel_detail, get_channels, get_profile, get_trending, get_user_profile, join_channel, leave_channel, like_tweet, load_feed, remove_project, rescore_project, set_avatar, setup_profile, unfollow_user, update_profile }
    core.social_graph --> core.site.jacyac.components.ChannelsTab { ChannelBundle, Tweet }
    core.social_graph --> core.site.jacyac.components.ExploreTab { Profile, Project }
    core.social_graph --> core.site.jacyac.components.FeedTab { Tweet }
    core.social_graph --> core.site.jacyac.components.ProfileEditor { Profile }
    core.social_graph --> core.site.jacyac.components.ProfileHeader { ProfileBundle }
    core.social_graph --> core.site.jacyac.components.ProjectCard { Project }
    core.social_graph --> core.site.jacyac.components.ProjectsPanel { Project }
    core.social_graph --> core.site.jacyac.components.RightSidebar { Profile, TrendingTag }
    core.social_graph --> core.site.jacyac.components.TweetCard { Tweet }
    core.timefmt --> core.install | core.social_graph { now_iso, seconds_since }
    core.timefmt --> core.leaderboard.scoring { days_since }
    core.timefmt --> core.progress | core.docs.sync { now_iso }
    core.utils --> core.site.docs.DocsSidebar { cn }
    core.utils --> core.site.docs.DocsTocRail { cn }
    core.utils --> core.site.jacyac.components.ExploreTab { cn }
    core.utils --> core.site.jacyac.components.MobileNav { cn }
    core.utils --> core.site.jacyac.components.ProjectCard { cn }
    core.utils --> core.site.jacyac.components.Sidebar { cn }
    core.utils --> core.site.jacyac.components.TweetCard { cn }
    core.utils --> core.site.landing.BookSection { cn }
    core.utils --> core.site.landing.CopyCommand { cn }
    core.utils --> core.site.landing.Hero { cn }
    core.utils --> core.site.ui.CodeBlock { cn }
    core.utils --> core.site.ui.Navbar { cn }
    core.utils --> core.site.ui.accordion { cn }
    core.utils --> core.site.ui.alert_dialog { cn }
    core.utils --> core.site.ui.avatar { cn }
    core.utils --> core.site.ui.badge { cn }
    core.utils --> core.site.ui.button { cn }
    core.utils --> core.site.ui.card { cn }
    core.utils --> core.site.ui.carousel { cn }
    core.utils --> core.site.ui.dialog { cn }
    core.utils --> core.site.ui.dropdown_menu { cn }
    core.utils --> core.site.ui.empty { cn }
    core.utils --> core.site.ui.field { cn }
    core.utils --> core.site.ui.hover_card { cn }
    core.utils --> core.site.ui.input { cn }
    core.utils --> core.site.ui.label { cn }
    core.utils --> core.site.ui.select { cn }
    core.utils --> core.site.ui.separator { cn }
    core.utils --> core.site.ui.skeleton { cn }
    core.utils --> core.site.ui.tabs { cn }
    core.utils --> core.site.ui.textarea { cn }
    core.utils --> core.site.ui.tooltip { cn }
    core.utils --> core.site.landing.Reveal | core.site.source.FloatingSource { cn }
    core.brand.font --> core.jacyac.native.JacYacMobile { useBrandFont }
    core.brand.logo --> core.brand.styles { logo_xml }
    core.brand.theme --> core.jacyac.native.JacYacMobile { useTheme }
    core.brand.theme --> core.jacyac.native.components.Avatar { useTheme }
    core.brand.theme --> core.jacyac.native.components.BridgeBanner { useTheme }
    core.brand.theme --> core.jacyac.native.components.Composer { useTheme }
    core.brand.theme --> core.jacyac.native.components.StatusView { useTheme }
    core.brand.theme --> core.jacyac.native.components.TabBar { useTheme }
    core.brand.theme --> core.jacyac.native.components.TweetCard { useTheme }
    core.brand.theme --> core.jacyac.native.screens.AuthScreen { useTheme }
    core.brand.theme --> core.jacyac.native.screens.ChannelsScreen { useTheme }
    core.brand.theme --> core.jacyac.native.screens.ExploreScreen { useTheme }
    core.brand.theme --> core.jacyac.native.screens.FeedScreen { useTheme }
    core.brand.theme --> core.jacyac.native.screens.ProfileScreen { useTheme }
    core.brand.theme --> core.jacyac.native.screens.ScoresScreen { useTheme }
    core.brand.theme --> core.site.ui.Navbar { useTheme }
    core.brand.tokens --> core.brand.styles { Colors, dark_palette, font_family, fonts, light_palette, radii, spacing }
    core.brand.tokens --> core.brand.theme { Colors, dark_palette, light_palette }
    core.brand.tokens --> core.jacyac.native.theme { Colors, font_family, fonts, radii, spacing }
    core.docs.graph --> cli.commands.docs { DocsStatus, docs_status }
    core.docs.graph --> core.docs.sync { DocVersion, DocsHub, HasHub, HasVersion, NextPage, _pretty, _sweep_stale, _version, place_page, rewrite_href, toc_of }
    core.docs.graph --> core.site.docs.DocsArticle { DocPageView }
    core.docs.graph --> core.site.docs.DocsGraphFloat { TreeNode }
    core.docs.graph --> core.site.docs.DocsShell { DocPageView, DocTree, DocsStatus, TreeNode, VersionInfo, doc_page, doc_tree, docs_status }
    core.docs.graph --> core.site.docs.DocsSidebar { TreeNode, VersionInfo }
    core.docs.graph --> core.site.docs.DocsTocRail { TocEntry }
    core.docs.graph --> web.main { doc_page, doc_tree, docs_status, llms_txt }
    core.docs.sync --> cli.commands.docs | web.main { docs_sync_tick }
    core.jacyac.format --> core.jacyac.identity { handle_of }
    core.jacyac.format --> core.jacyac.native.components.Avatar { handle_of, initial_of }
    core.jacyac.format --> core.jacyac.native.components.TweetCard { handle_of }
    core.jacyac.format --> core.jacyac.native.screens.ChannelsScreen { count_label }
    core.jacyac.format --> core.jacyac.native.screens.ExploreScreen { handle_of }
    core.jacyac.format --> core.jacyac.native.screens.ProfileScreen { handle_of }
    core.jacyac.format --> core.site.jacyac.components.ExploreTab { handle_of, initial_of }
    core.jacyac.format --> core.site.jacyac.components.ProfileHeader { handle_of, initial_of }
    core.jacyac.format --> core.site.jacyac.components.ProjectCard { handle_of, initial_of }
    core.jacyac.format --> core.site.jacyac.components.RightSidebar { handle_of, initial_of }
    core.jacyac.format --> core.site.jacyac.components.Sidebar { handle_of }
    core.jacyac.format --> core.site.jacyac.components.TweetCard { handle_of, initial_of }
    core.jacyac.genius --> core.social_graph { GuideSample, optional_fact, random_guide }
    core.jacyac.identity --> core.jacyac.native.components.Avatar { avatar_of }
    core.jacyac.identity --> core.jacyac.native.screens.ExploreScreen { name_of }
    core.jacyac.identity --> core.jacyac.native.screens.ProfileScreen { name_of }
    core.jacyac.identity --> core.jacyac.state { project_error_message }
    core.jacyac.identity --> core.site.jacyac.JacYac { avatar_of, name_of }
    core.jacyac.identity --> core.site.jacyac.components.ExploreTab { avatar_of, name_of }
    core.jacyac.identity --> core.site.jacyac.components.ProfileHeader { avatar_of, name_of }
    core.jacyac.identity --> core.site.jacyac.components.ProjectCard { avatar_of, project_error_message }
    core.jacyac.identity --> core.site.jacyac.components.RightSidebar { avatar_of, name_of }
    core.jacyac.identity --> core.site.jacyac.components.TweetCard { avatar_of }
    core.jacyac.limits --> cli.commands.feed { PostingDenied }
    core.jacyac.limits --> core.social_graph { PostingDenied, posting_limit }
    core.jacyac.registration --> core.jacyac.session { register_with_challenge }
    core.jacyac.scores --> core.jacyac.native.screens.ScoresScreen { useScores }
    core.jacyac.scores --> core.site.jacyac.components.NinjaScores { useScores }
    core.jacyac.session --> core.jacyac.state { Session, stored_username, useSession }
    core.jacyac.state --> core.jacyac.native.JacYacMobile | core.site.jacyac.JacYac { useJacYac }
    core.jacyac.state --> core.jacyac.native.screens.ScoresScreen { JacYacState }
    core.jacyac.state --> core.jacyac.scores { JacYacState }
    core.jacyac.state --> core.site.jacyac.components.NinjaScores { JacYacState }
    core.jacyac.validation --> core.jacyac.native.components.Composer { chars_left }
    core.jacyac.validation --> core.site.jacyac.components.Composer { chars_left, post_limit, valid_post }
    core.jacyac.validation --> core.social_graph | core.jacyac.state { valid_post }
    core.jacyac.github.auth --> core.jacyac.github.login { begin_github, finish_github }
    core.jacyac.github.auth --> core.jacyac.github.repos { github_id }
    core.jacyac.github.auth --> core.jacyac.session { github_enabled }
    core.jacyac.github.auth --> core.site.jacyac.GithubCallback { complete_native_github, github_callback_mode }
    core.jacyac.github.auth --> core.social_graph { users }
    core.jacyac.github.auth --> desktop.main { begin_github, complete_native_github, finish_github, github_callback_mode, github_enabled, poll_github }
    core.jacyac.github.auth --> web.main { begin_github, complete_native_github, finish_github, github_callback_mode, github_enabled, poll_github }
    core.jacyac.github.login --> core.jacyac.session { github_login }
    core.jacyac.github.login --> core.site.jacyac.GithubCallback { complete_web_login }
    core.jacyac.github.repos --> core.jacyac.scores { GithubRepo, github_repositories }
    core.jacyac.github.repos --> core.social_graph { verified_owner }
    core.jacyac.github.repos --> desktop.main | web.main { github_repositories }
    core.jacyac.native.JacYacMobile --> core.site.landing.MobileShowcase | mobile.main { JacYacMobile }
    core.jacyac.native.icon --> core.jacyac.native.JacYacMobile { Icon }
    core.jacyac.native.icon --> core.jacyac.native.components.BridgeBanner { Icon }
    core.jacyac.native.icon --> core.jacyac.native.components.StatusView { Icon }
    core.jacyac.native.icon --> core.jacyac.native.components.TabBar { Icon }
    core.jacyac.native.icon --> core.jacyac.native.components.TweetCard { Icon }
    core.jacyac.native.icon --> core.jacyac.native.screens.AuthScreen { Icon }
    core.jacyac.native.icon --> core.jacyac.native.screens.ChannelsScreen { Icon }
    core.jacyac.native.icon --> core.jacyac.native.screens.ExploreScreen { Icon }
    core.jacyac.native.icon --> core.jacyac.native.screens.FeedScreen { Icon }
    core.jacyac.native.icon --> core.jacyac.native.screens.ProfileScreen { Icon }
    core.jacyac.native.theme --> core.jacyac.native.JacYacMobile { makeStyles }
    core.jacyac.native.theme --> core.jacyac.native.components.Avatar { makeStyles }
    core.jacyac.native.theme --> core.jacyac.native.components.BridgeBanner { makeStyles }
    core.jacyac.native.theme --> core.jacyac.native.components.Composer { makeStyles }
    core.jacyac.native.theme --> core.jacyac.native.components.StatusView { makeStyles }
    core.jacyac.native.theme --> core.jacyac.native.components.TabBar { makeStyles }
    core.jacyac.native.theme --> core.jacyac.native.components.TweetCard { makeStyles }
    core.jacyac.native.theme --> core.jacyac.native.screens.AuthScreen { makeStyles }
    core.jacyac.native.theme --> core.jacyac.native.screens.ChannelsScreen { makeStyles }
    core.jacyac.native.theme --> core.jacyac.native.screens.ExploreScreen { makeStyles }
    core.jacyac.native.theme --> core.jacyac.native.screens.FeedScreen { makeStyles }
    core.jacyac.native.theme --> core.jacyac.native.screens.ProfileScreen { makeStyles }
    core.jacyac.native.theme --> core.jacyac.native.screens.ScoresScreen { makeStyles }
    core.jacyac.native.components.Avatar --> core.jacyac.native.components.Composer { Avatar }
    core.jacyac.native.components.Avatar --> core.jacyac.native.components.TweetCard { Avatar }
    core.jacyac.native.components.Avatar --> core.jacyac.native.screens.ExploreScreen { Avatar }
    core.jacyac.native.components.Avatar --> core.jacyac.native.screens.ProfileScreen { Avatar }
    core.jacyac.native.components.BrandMark --> core.jacyac.native.JacYacMobile { BrandMark }
    core.jacyac.native.components.BrandMark --> core.jacyac.native.screens.AuthScreen { BrandMark }
    core.jacyac.native.components.BridgeBanner --> core.jacyac.native.JacYacMobile { BridgeBanner }
    core.jacyac.native.components.Composer --> core.jacyac.native.screens.ChannelsScreen { Composer }
    core.jacyac.native.components.Composer --> core.jacyac.native.screens.FeedScreen { Composer }
    core.jacyac.native.components.StatusView --> core.jacyac.native.screens.ChannelsScreen { EmptyState, LoadingRows }
    core.jacyac.native.components.StatusView --> core.jacyac.native.screens.ExploreScreen { EmptyState, LoadingRows }
    core.jacyac.native.components.StatusView --> core.jacyac.native.screens.FeedScreen { EmptyState, LoadingRows }
    core.jacyac.native.components.StatusView --> core.jacyac.native.screens.ProfileScreen { EmptyState }
    core.jacyac.native.components.TabBar --> core.jacyac.native.JacYacMobile { TabBar }
    core.jacyac.native.components.TweetCard --> core.jacyac.native.screens.ChannelsScreen { TweetCard }
    core.jacyac.native.components.TweetCard --> core.jacyac.native.screens.FeedScreen { TweetCard }
    core.jacyac.native.components.TweetCard --> core.jacyac.native.screens.ProfileScreen { TweetCard }
    core.jacyac.native.screens.AuthScreen --> core.jacyac.native.JacYacMobile { AuthScreen }
    core.jacyac.native.screens.ChannelsScreen --> core.jacyac.native.JacYacMobile { ChannelsScreen }
    core.jacyac.native.screens.ExploreScreen --> core.jacyac.native.JacYacMobile { ExploreScreen }
    core.jacyac.native.screens.FeedScreen --> core.jacyac.native.JacYacMobile { FeedScreen }
    core.jacyac.native.screens.ProfileScreen --> core.jacyac.native.JacYacMobile { ProfileScreen }
    core.jacyac.native.screens.ScoresScreen --> core.jacyac.native.JacYacMobile { ScoresScreen }
    core.leaderboard.board --> core.social_graph { BoardHub, OnBoard, RepoEntry }
    core.leaderboard.format --> core.site.jacyac.components.ProjectCard { belt_class, belt_label, time_ago }
    core.leaderboard.format --> core.site.leaderboard.Methodology { belt_class, belt_label }
    core.leaderboard.scoring --> cli.commands.score { RepoAnalysis, ScoreBreakdown, analyze, score }
    core.leaderboard.scoring --> core.leaderboard.board { RepoFeatures, ScoreBreakdown }
    core.leaderboard.scoring --> core.scoring_service { RepoAnalysis, ScoreBreakdown, analyze, score }
    core.leaderboard.scoring --> core.social_graph { ScoreBreakdown }
    core.packages.catalog --> core.site.packages.ApiDocs { ApiMember, ApiModule, ApiParam, ApiSymbol }
    core.packages.catalog --> core.site.packages.PackagePage { PackageDetail, PackageVersion }
    core.packages.catalog --> core.site.packages.PackagesIndex { PackageCatalog, PackageSummary }
    core.packages.catalog --> core.site.packages.PackagesShell { PackageCatalog, PackageDetail, package_catalog, package_detail }
    core.packages.catalog --> web.main { package_catalog, package_detail }
    core.site.docs.DocsArticle --> core.site.docs.DocsShell { DocsArticle, DocsArticleSkeleton }
    core.site.docs.DocsGraphFloat --> core.site.docs.DocsSidebar { DocsGraphFloat }
    core.site.docs.DocsShell --> desktop.pages.docs.index | web.pages.docs.index { DocsShell }
    core.site.docs.DocsSidebar --> core.site.docs.DocsShell { DocsSidebar }
    core.site.docs.DocsTocRail --> core.site.docs.DocsShell { DocsTocRail }
    core.site.docs.Markdown --> core.site.docs.DocsArticle | core.site.packages.PackagePage { Markdown }
    core.site.docs.MermaidDiagram --> core.site.docs.Markdown { MermaidDiagram }
    core.site.game.webgl_host --> core.site.landing.WasmGame { run_game }
    core.site.game.arena --> core.site.game.webgl_host { frame, get_deaths, get_hp, get_score, init, shutdown }
    core.site.game.gmath --> core.site.game.arena { clampf, jsin, lerp }
    core.site.game.gmath --> core.site.game.sim { DEG2RAD, Rng, jcos, jsin, jsqrt, rand01, rand_range, rand_sign }
    core.site.game.platform_rl --> core.site.game.arena { KEY_A, KEY_D, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_S, KEY_SPACE, KEY_TAB, KEY_UP, KEY_W, MOUSE_LEFT, SCREEN_H, SCREEN_W, begin_frame, begin_model, begin_overlay, close_window, draw_box, draw_floor, draw_fps, draw_rect2d, end_frame, end_model, frame_dt, key_held, key_tapped, lock_mouse, mouse_pressed, mouse_x, mouse_y, open_window, set_camera, should_close, unlock_mouse }
    core.site.game.sim --> core.site.game.arena { CHARGE_T, Cmd, EnemyPool, FIRE_COOLDOWN, Game, HP_MAX, MAX_ENEMIES, PITCH_LIMIT, Player, ProjectilePool, SparkPool, Stats, TICK_DT, TICK_MAX_CATCHUP, sim_tick, world_new }
    type core.site.game.sim --> core.site.game.webgl_host { Game }
    core.site.jacyac.GithubCallback --> desktop.pages.jacyac.github.callback { GithubCallback }
    core.site.jacyac.GithubCallback --> web.pages.jacyac.github.callback { GithubCallback }
    core.site.jacyac.JacYac --> desktop.pages.jacyac { JacYac }
    core.site.jacyac.JacYac --> desktop.pages.jacyac.scores { JacYac }
    core.site.jacyac.JacYac --> desktop.pages.socialize { JacYac }
    core.site.jacyac.JacYac --> web.pages.jacyac { JacYac }
    core.site.jacyac.JacYac --> web.pages.jacyac.scores { JacYac }
    core.site.jacyac.JacYac --> web.pages.socialize { JacYac }
    core.site.jacyac.components.AuthForm --> core.site.jacyac.JacYac { AuthForm }
    core.site.jacyac.components.ChannelsTab --> core.site.jacyac.JacYac { ChannelsTab }
    core.site.jacyac.components.Composer --> core.site.jacyac.components.ChannelsTab { Composer }
    core.site.jacyac.components.Composer --> core.site.jacyac.components.FeedTab { Composer }
    core.site.jacyac.components.ExploreTab --> core.site.jacyac.JacYac { ExploreTab }
    core.site.jacyac.components.FeedTab --> core.site.jacyac.JacYac { FeedTab }
    core.site.jacyac.components.MobileNav --> core.site.jacyac.JacYac { MobileNav }
    core.site.jacyac.components.NinjaScores --> core.site.jacyac.JacYac { NinjaScores }
    core.site.jacyac.components.ProfileEditor --> core.site.jacyac.JacYac { ProfileEditor }
    core.site.jacyac.components.ProfileHeader --> core.site.jacyac.JacYac { ProfileHeader }
    core.site.jacyac.components.ProjectCard --> core.site.jacyac.components.ExploreTab { ProjectCard }
    core.site.jacyac.components.ProjectCard --> core.site.jacyac.components.NinjaScores { ProjectCard }
    core.site.jacyac.components.ProjectCard --> core.site.jacyac.components.ProjectsPanel { ProjectCard }
    core.site.jacyac.components.ProjectsPanel --> core.site.jacyac.JacYac { ProjectsPanel }
    core.site.jacyac.components.RightSidebar --> core.site.jacyac.JacYac { RightSidebar }
    core.site.jacyac.components.Sidebar --> core.site.jacyac.JacYac { Sidebar }
    core.site.jacyac.components.TweetCard --> core.site.jacyac.JacYac { TweetCard }
    core.site.jacyac.components.TweetCard --> core.site.jacyac.components.ChannelsTab { TweetCard }
    core.site.jacyac.components.TweetCard --> core.site.jacyac.components.FeedTab { TweetCard }
    core.site.jacyac.components.WelcomeBanner --> core.site.jacyac.components.FeedTab { WelcomeBanner }
    core.site.landing.Agents --> core.site.landing.Home { Agents }
    core.site.landing.BookSection --> core.site.landing.Home { BookSection }
    core.site.landing.Capabilities --> core.site.landing.Home { Capabilities }
    core.site.landing.CopyCommand --> core.site.landing.Agents | core.site.landing.Hero { CopyCommand }
    core.site.landing.CopyCommand --> core.site.landing.ExplorerFinale { CopyCommandBlock }
    core.site.landing.CopyCommand --> core.site.packages.PackagePage | core.site.packages.PackagesIndex { CopyCommand }
    core.site.landing.ExplorerFinale --> core.site.landing.Home { ExplorerFinale }
    core.site.landing.Hero --> core.site.landing.Home { Hero }
    core.site.landing.Home --> desktop.pages.index | web.pages.index { Home }
    core.site.landing.MobileShowcase --> core.site.landing.Home { MobileShowcase }
    core.site.landing.OneBinary --> core.site.landing.Home { OneBinary }
    core.site.landing.Reveal --> core.site.landing.Agents { Reveal }
    core.site.landing.Reveal --> core.site.landing.BookSection { Reveal }
    core.site.landing.Reveal --> core.site.landing.Capabilities { Reveal }
    core.site.landing.Reveal --> core.site.landing.ExplorerFinale { Reveal }
    core.site.landing.Reveal --> core.site.landing.MobileShowcase { Reveal }
    core.site.landing.Reveal --> core.site.landing.OneBinary { Reveal }
    core.site.landing.Reveal --> core.site.landing.Showcase { Reveal }
    core.site.landing.Reveal --> core.site.landing.StatsBand { Reveal }
    core.site.landing.Reveal --> core.site.landing.WaitWuuut { Reveal }
    core.site.landing.Reveal --> core.site.landing.WasmGame { Reveal }
    core.site.landing.Reveal --> core.site.landing.WhyJac { Reveal }
    core.site.landing.Showcase --> core.site.landing.Home { Showcase }
    core.site.landing.StatsBand --> core.site.landing.Home { StatsBand }
    core.site.landing.WasmGame --> core.site.landing.Home { WasmGame }
    core.site.landing.WhyJac --> core.site.landing.Capabilities { WhySlide }
    core.site.landing.WhyJac --> core.site.landing.Home { WhyJac }
    core.site.landing.diagrams.GradualBorrowDiagram --> core.site.landing.WaitWuuut { GradualBorrowDiagram }
    core.site.landing.diagrams.GradualBorrowDiagram --> core.site.landing.WhyJac { GradualBorrowDiagram }
    core.site.landing.diagrams.PolypilerDiagram --> core.site.landing.OneBinary { PolypilerDiagram }
    core.site.landing.diagrams.PolypilerDiagram --> core.site.landing.WaitWuuut { PolypilerDiagram }
    core.site.landing.diagrams.SynechicDiagram --> core.site.landing.WaitWuuut { SynechicDiagram }
    core.site.landing.diagrams.SynechicDiagram --> core.site.landing.WhyJac { SynechicDiagram }
    core.site.landing.diagrams.TopokineticDiagram --> core.site.landing.WaitWuuut { TopokineticDiagram }
    core.site.landing.diagrams.TopokineticDiagram --> core.site.landing.WhyJac { TopokineticDiagram }
    core.site.landing.diagrams.motion --> core.site.landing.diagrams.GradualBorrowDiagram { view_once }
    core.site.landing.diagrams.motion --> core.site.landing.diagrams.PolypilerDiagram { view_once }
    core.site.landing.diagrams.motion --> core.site.landing.diagrams.SynechicDiagram { view_once }
    core.site.landing.diagrams.motion --> core.site.landing.diagrams.TopokineticDiagram { view_once }
    core.site.leaderboard.Methodology --> core.site.jacyac.components.NinjaScores { Methodology }
    core.site.leaderboard.Methodology --> desktop.pages.methodology { Methodology }
    core.site.leaderboard.Methodology --> web.pages.methodology { Methodology }
    core.site.packages.ApiDocs --> core.site.packages.PackagePage { ApiDocs }
    core.site.packages.PackagePage --> core.site.packages.PackagesShell { PackagePage }
    core.site.packages.PackagesIndex --> core.site.packages.PackagesShell { PackagesIndex }
    core.site.packages.PackagesShell --> desktop.pages.packages.index | web.pages.packages.index { PackagesShell }
    core.site.source.CodeSpotlight --> core.site.landing.MobileShowcase { CodeSpotlight }
    core.site.source.CodeSpotlight --> core.site.landing.WaitWuuut { CodeSpotlight }
    core.site.source.FloatingSource --> core.site.landing.Hero { FloatingSource }
    core.site.source.FloatingSource --> core.site.landing.WaitWuuut { FloatingSource }
    core.site.source.SourceBrowser --> core.site.landing.ExplorerFinale { SourceBrowser }
    core.site.source.SourceBrowser --> core.site.source.FloatingSource { SourceBrowser }
    core.site.ui.CodeBlock --> core.site.docs.Markdown { CodeLines }
    core.site.ui.CodeBlock --> core.site.docs.MermaidDiagram { CodeLines }
    core.site.ui.CodeBlock --> core.site.landing.Showcase { CodeBlock }
    core.site.ui.CodeBlock --> core.site.source.CodeSpotlight { CodeLines }
    core.site.ui.CodeBlock --> core.site.source.SourceBrowser { CodeLines }
    core.site.ui.Footer --> core.site.ui.SiteShell { Footer }
    core.site.ui.GraphBackdrop --> core.site.docs.DocsShell { GraphBackdrop }
    core.site.ui.GraphBackdrop --> core.site.landing.Hero { GraphBackdrop }
    core.site.ui.GraphBackdrop --> core.site.leaderboard.Methodology { GraphBackdrop }
    core.site.ui.GraphBackdrop --> core.site.ui.NotFound { GraphBackdrop }
    core.site.ui.Navbar --> core.site.ui.SiteShell { Navbar }
    core.site.ui.SectionRail --> core.site.landing.Home | core.site.landing.WaitWuuut { SectionRail }
    core.site.ui.SiteShell --> desktop.pages.layout | web.pages.layout { SiteShell }
    core.site.ui.alert_dialog --> core.site.jacyac.components.ProjectCard { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger }
    core.site.ui.alert_dialog --> core.site.jacyac.components.TweetCard { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger }
    core.site.ui.avatar --> core.site.jacyac.components.Composer { Avatar, AvatarFallback, AvatarImage }
    core.site.ui.avatar --> core.site.jacyac.components.ExploreTab { Avatar, AvatarFallback, AvatarImage }
    core.site.ui.avatar --> core.site.jacyac.components.ProfileHeader { Avatar, AvatarFallback, AvatarImage }
    core.site.ui.avatar --> core.site.jacyac.components.ProjectCard { Avatar, AvatarFallback, AvatarImage }
    core.site.ui.avatar --> core.site.jacyac.components.RightSidebar { Avatar, AvatarFallback, AvatarImage }
    core.site.ui.avatar --> core.site.jacyac.components.Sidebar { Avatar, AvatarFallback, AvatarImage }
    core.site.ui.avatar --> core.site.jacyac.components.TweetCard { Avatar, AvatarFallback, AvatarImage }
    core.site.ui.badge --> core.site.jacyac.components.ChannelsTab { Badge }
    core.site.ui.badge --> core.site.jacyac.components.ProjectCard { Badge }
    core.site.ui.badge --> core.site.jacyac.components.RightSidebar { Badge }
    core.site.ui.badge --> core.site.jacyac.components.Sidebar { Badge }
    core.site.ui.badge --> core.site.landing.Agents { Badge }
    core.site.ui.badge --> core.site.landing.BookSection { Badge }
    core.site.ui.badge --> core.site.landing.ExplorerFinale { Badge }
    core.site.ui.badge --> core.site.landing.Hero { Badge }
    core.site.ui.badge --> core.site.landing.MobileShowcase { Badge }
    core.site.ui.badge --> core.site.landing.OneBinary { Badge }
    core.site.ui.badge --> core.site.landing.Showcase { Badge }
    core.site.ui.badge --> core.site.landing.WaitWuuut { Badge }
    core.site.ui.badge --> core.site.landing.WasmGame { Badge }
    core.site.ui.badge --> core.site.landing.WhyJac { Badge }
    core.site.ui.badge --> core.site.leaderboard.Methodology { Badge }
    core.site.ui.badge --> core.site.packages.PackagePage | core.site.packages.PackagesIndex { Badge }
    core.site.ui.button --> core.site.jacyac.JacYac { Button }
    core.site.ui.button --> core.site.jacyac.components.AuthForm { Button }
    core.site.ui.button --> core.site.jacyac.components.ChannelsTab { Button }
    core.site.ui.button --> core.site.jacyac.components.Composer { Button }
    core.site.ui.button --> core.site.jacyac.components.ExploreTab { Button }
    core.site.ui.button --> core.site.jacyac.components.NinjaScores { Button }
    core.site.ui.button --> core.site.jacyac.components.ProfileEditor { Button }
    core.site.ui.button --> core.site.jacyac.components.ProfileHeader { Button }
    core.site.ui.button --> core.site.jacyac.components.ProjectCard { Button }
    core.site.ui.button --> core.site.jacyac.components.ProjectsPanel { Button }
    core.site.ui.button --> core.site.jacyac.components.RightSidebar { Button }
    core.site.ui.button --> core.site.jacyac.components.Sidebar { Button }
    core.site.ui.button --> core.site.jacyac.components.TweetCard { Button }
    core.site.ui.button --> core.site.jacyac.components.WelcomeBanner { Button }
    core.site.ui.button --> core.site.landing.BookSection { buttonVariants }
    core.site.ui.button --> core.site.landing.ExplorerFinale { buttonVariants }
    core.site.ui.button --> core.site.landing.Hero { buttonVariants }
    core.site.ui.button --> core.site.landing.WasmGame { Button }
    core.site.ui.button --> core.site.ui.Navbar { buttonVariants }
    core.site.ui.button --> core.site.ui.NotFound { buttonVariants }
    core.site.ui.button --> core.site.ui.alert_dialog { Button }
    core.site.ui.button --> core.site.ui.carousel { Button }
    core.site.ui.button --> core.site.ui.dialog { buttonVariants }
    core.site.ui.card --> core.site.jacyac.components.AuthForm { Card, CardContent, CardDescription, CardHeader, CardTitle }
    core.site.ui.card --> core.site.jacyac.components.RightSidebar { Card, CardContent, CardHeader, CardTitle }
    core.site.ui.card --> core.site.landing.Capabilities { Card, CardContent, CardHeader, CardTitle }
    core.site.ui.carousel --> core.site.landing.Capabilities { Carousel, CarouselContent, CarouselDots, CarouselItem, CarouselNext, CarouselPrevious }
    core.site.ui.carousel --> core.site.landing.WhyJac { Carousel, CarouselContent, CarouselDots, CarouselItem, CarouselNext, CarouselPrevious }
    core.site.ui.dialog --> core.site.jacyac.components.ChannelsTab { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle }
    core.site.ui.dropdown_menu --> core.site.jacyac.components.Sidebar { DropdownMenu, DropdownMenuContent, DropdownMenuGroup, DropdownMenuItem, DropdownMenuTrigger }
    core.site.ui.empty --> core.site.jacyac.components.ChannelsTab { Empty, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle }
    core.site.ui.empty --> core.site.jacyac.components.ExploreTab { Empty, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle }
    core.site.ui.empty --> core.site.jacyac.components.FeedTab { Empty, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle }
    core.site.ui.field --> core.site.jacyac.components.AuthForm { Field, FieldLabel }
    core.site.ui.field --> core.site.jacyac.components.ChannelsTab { Field, FieldLabel }
    core.site.ui.field --> core.site.jacyac.components.ProfileEditor { Field, FieldLabel }
    core.site.ui.hover_card --> core.site.jacyac.components.RightSidebar { HoverCard, HoverCardContent, HoverCardTrigger }
    core.site.ui.input --> core.site.docs.DocsSidebar { Input }
    core.site.ui.input --> core.site.jacyac.components.AuthForm { Input }
    core.site.ui.input --> core.site.jacyac.components.ChannelsTab { Input }
    core.site.ui.input --> core.site.jacyac.components.NinjaScores { Input }
    core.site.ui.input --> core.site.jacyac.components.ProfileEditor { Input }
    core.site.ui.input --> core.site.jacyac.components.ProjectsPanel { Input }
    core.site.ui.input --> core.site.jacyac.components.RightSidebar { Input }
    core.site.ui.input --> core.site.jacyac.components.TweetCard { Input }
    core.site.ui.input --> core.site.packages.PackagesIndex { Input }
    core.site.ui.label --> core.site.ui.field { Label }
    core.site.ui.select --> core.site.docs.DocsSidebar { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue }
    core.site.ui.separator --> core.site.ui.field { Separator }
    core.site.ui.skeleton --> core.site.docs.DocsArticle { Skeleton }
    core.site.ui.skeleton --> core.site.docs.DocsSidebar { Skeleton }
    core.site.ui.skeleton --> core.site.jacyac.components.ChannelsTab { Skeleton }
    core.site.ui.skeleton --> core.site.jacyac.components.ExploreTab { Skeleton }
    core.site.ui.skeleton --> core.site.jacyac.components.FeedTab { Skeleton }
    core.site.ui.tabs --> core.site.docs.Markdown { Tabs, TabsContent, TabsList, TabsTrigger }
    core.site.ui.tabs --> core.site.landing.Showcase { Tabs, TabsContent, TabsList, TabsTrigger }
    core.site.ui.textarea --> core.site.jacyac.components.ChannelsTab { Textarea }
    core.site.ui.textarea --> core.site.jacyac.components.Composer { Textarea }
    core.site.ui.textarea --> core.site.jacyac.components.ProfileEditor { Textarea }
    core.site.ui.tooltip --> core.site.jacyac.components.TweetCard { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger }
    core.source.files --> core.site.landing.Showcase { SourceView, example_sources }
    core.source.files --> core.site.source.CodeSpotlight { SourceSpan, source_span }
    core.source.files --> core.site.source.SourceBrowser { SourceFile, SourceView, source_file, source_tree }
    core.source.files --> web.main { SourceFile, SourceSpan, SourceView, example_sources, source_file, source_span, source_tree }
}
