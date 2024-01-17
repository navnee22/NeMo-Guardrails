# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Optional

from pydantic import BaseModel, Field


class LLMCallInfo(BaseModel):
    task: Optional[str] = Field(
        default=None, description="The internal task that made the call."
    )
    prompt: Optional[str] = Field(
        default=None, description="The prompt that was used for the LLM call."
    )
    completion: Optional[str] = Field(
        default=None, description="The completion generated by the LLM."
    )
    duration: Optional[float] = Field(
        default=None, description="The duration in seconds."
    )
    total_tokens: Optional[int] = Field(
        default=None, description="The total number of used tokens."
    )
    prompt_tokens: Optional[int] = Field(
        default=None, description="The number of input tokens."
    )
    completion_tokens: Optional[int] = Field(
        default=None, description="The number of output tokens."
    )


class ExplainInfo(BaseModel):
    """Object that holds additional explanation information.

    This is useful for debugging end educational purposes.
    """

    llm_calls: List[LLMCallInfo] = Field(
        default_factory=list,
        description="The list of LLM calls that have been made to fulfill the generation request.",
    )

    colang_history: Optional[str] = Field(
        default=None,
        description="The history of the conversation written in Colang format.",
    )

    def print_llm_calls_summary(self):
        """Helper to print a quick overview of the LLM calls that were made."""

        if len(self.llm_calls) == 0:
            print("No LLM calls were made.")

        else:
            total_duration = 0
            total_tokens = 0
            for llm_call in self.llm_calls:
                total_duration += llm_call.duration or 0
                total_tokens += llm_call.total_tokens or 0

            msg = (
                f"Summary: {len(self.llm_calls)} LLM call(s) took {total_duration:.2f} seconds "
                + (f"and used {total_tokens} tokens.\n" if total_tokens else ".\n")
            )

            print(msg)

            for i in range(len(self.llm_calls)):
                llm_call = self.llm_calls[i]
                msg = (
                    f"{i+1}. Task `{llm_call.task}` took {llm_call.duration:.2f} seconds "
                    + (
                        f"and used {llm_call.total_tokens} tokens."
                        if total_tokens
                        else "."
                    )
                )
                print(msg)

            print("")
